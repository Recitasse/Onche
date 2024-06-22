from dataclasses import dataclass
from typing import ClassVar, List, Union
import subprocess
import sys
from .process import Process
import os


@dataclass(init=True, order=False, repr=True, slots=True)
class ProcessManager:
    list_pid_running: ClassVar[List[int]] = []
    system: ClassVar[set] = {'linux', 'win'}

    @staticmethod
    def __post_init__():
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            ProcessManager.system.discard('win')
        elif sys.platform.startswith('win'):
            ProcessManager.system.discard('linux')
        else:
            TypeError(f"Le système : {sys.platform} n'est pas pris en compte")

    @classmethod
    def kill_process(cls, process: Process) -> None:
        """
        Tue un processus s'il est en execution
        :param process: le nom precessus à tuer
        :return:
        """
        if not cls._check_running(process):
            return

        if process not in cls.list_pid_running:
            raise ValueError("Le processus n'est pas dans la liste")

        if 'linux' in cls.system:
            try:
                subprocess.run(['kill', str(process.pid)], check=True)
                cls.list_pid_running.remove(process.pid)
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de la tentative de terminaison du processus {process.pid}: {e}")
        elif 'win' in cls.system:
            try:
                subprocess.run(['taskkill', '/PID', str(process.pid), '/F'], check=True)
                cls.list_pid_running.remove(process.pid)
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de la tentative de terminaison du processus {process.pid}: {e}")

    @classmethod
    def execute_process(cls, process: Process, take_output: bool = False) -> Union[tuple, None]:
        """
        Execute le processus
        :param process: le processus
        :param take_output: Si True, récupère la sortie
        :return: None
        """
        results = None
        if process.is_script:
            if 'linux' in cls.system:
                assert process.command.endswith('.sh') is True, "Ce n'est pas un script pour linux"
            elif 'win' in cls.system:
                assert process.command.endswith('.bat') is True, "Ce n'est pas un script pour windows"
            try:
                with subprocess.Popen([process.command], text=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as proc:
                    print(f"Process ID: {proc.pid}")
                    process.pid = proc.pid
                    results = proc.communicate()
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            try:
                result = subprocess.run(process.command, shell=True, text=True, capture_output=True, check=True)
                print("Output:", result.stdout)
            except subprocess.CalledProcessError as e:
                print("Error:", e.stderr)
            except Exception as e:
                print("An unexpected error occurred:", str(e))

        if cls._check_running(process) and process.pid != 0:
            cls.list_pid_running.append(process.pid)
        if take_output:
            return results
        return None

    @classmethod
    def _check_running(cls, process: Process) -> bool:
        """
        Check si un processus tourne
        :param process: le processus
        :return: True si le processus tourne
        """
        if 'linux' in cls.system:
            if process.pid is None:
                return False
            try:
                os.kill(process.pid, 0)
            except OSError:
                return False
            else:
                return True

        elif 'win' in cls.system:
            cmd = ['tasklist', '/FI', f'PID eq {process.pid}']
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if str(process.pid) in result.stdout:
                    return True
                return False
            except subprocess.SubprocessError as e:
                print(f"Failed to check process: {e}")
                return False

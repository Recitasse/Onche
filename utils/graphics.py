import time
import sys
import numpy as np

def update_prog_bar(titre, prog, total, points=50):
    prog_percent = prog / total
    bar_points = int(points * prog_percent)
    if prog_percent == 1.0:
        bar = f'{titre+" : "}[' + '=' * bar_points + ' ' * (points - bar_points) + ']'
    else:
        bar = f'{titre+" : "}[' + '=' * bar_points + '|' + ' ' * (points - bar_points) + ']'
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()

def bar(delais:int, titre:str="page")->None:
    """
    Objet graphique montrant une barre de progression (dépend du temps)

    Args:
        delais (int) : le temps total à attendre
        titre (string) : nom du processus (rien par défaut)
    """
    start = 0
    end = 100
    interval = delais/end

    for i in range(start, end + 1):
        update_prog_bar(titre, i - start, end - start)
        time.sleep(interval)
    print(f"\n{titre + ' =>'} processus terminé.")

def bar_etape(nbe:int, et:int, titre:str='page'):
    """
    Affiche la progression

    Args:
        nbe (int) : nombre étape (total)
        et (int) : l'étape actuelle
    """
    sys.stdout.write(f'\r{titre} {et+1}/{nbe} : \033[1m{np.round((et+1)/nbe*100,2)}%\033[0m.')
    sys.stdout.flush()
    if et == nbe-1 and titre != "page":
        sys.stdout.write(f'\rpage {nbe}/{nbe} : \033[1m100%\033[0m.')
        sys.stdout.flush()
        print("\n\tRécupération terminée.")
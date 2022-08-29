import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as py
import os


def read_summary_csv(csv_file):
    df = pd.read_csv(csv_file)
    df = df.drop([50])  # Drop the Mean row

    y_time_urts = df['urts_total_time'].to_numpy()
    y_time_ekstazi_ext = df['safe_total_time'].to_numpy()
    y_time_ekstazi_unsafe = df['unsafe_total_time'].to_numpy()
    y_time_retestall = df['retestall_total_time'].to_numpy()
    
    y_classes_urts = df['urts_total_classes'].to_numpy()
    y_classes_ekstazi_ext = df['safe_total_classes'].to_numpy()
    y_classes_ekstazi_unsafe = df['unsafe_total_classes'].to_numpy()
    y_classes_retestall = df['retestall_total_classes'].to_numpy()

    y_time = [y_time_urts, y_time_ekstazi_ext, y_time_ekstazi_unsafe, y_time_retestall]
    y_classes = [y_classes_urts, y_classes_ekstazi_ext, y_classes_ekstazi_unsafe, y_classes_retestall]
    print(y_time)
    return [y_time, y_classes]


def draw_helper(mode, target_file, y):
    fig, ax = plt.subplots(figsize=(9,6), dpi=100)
    x = [i for i in range(-49, 1)]
    
    ax.plot(x, y[0], label='uRTS', color='red', linestyle='solid', marker='.', markersize='15', markeredgecolor='k',markeredgewidth=1)
    ax.plot(x, y[1], label='Ekstazi-Ext', color='green', linestyle='solid',  marker='.', markersize='15')
    ax.plot(x, y[2], label='Ekstazi-Unsafe', color='blue', linestyle='solid', marker='.', markersize='15', markeredgecolor='k',markeredgewidth=1)
    ax.plot(x, y[3], label='ReTestAll', color='black', linestyle='solid', marker='.',  markersize='15', markeredgecolor='k',markeredgewidth=0.2)
    
    if mode == "num":
        ax.set_xlabel('Revision', fontproperties='Times New Roman', fontsize=35)
        ax.set_ylabel('# Test Classes', fontproperties='Times New Roman', fontsize=35)
    elif mode == "time":
        ax.set_xlabel('Revision', fontproperties='Times New Roman', fontsize=35)
        ax.set_ylabel('Time [sec]', fontproperties='Times New Roman', fontsize=35)
        
    ax.set_ylim(bottom=0.)
    ax.tick_params(axis='both', labelsize=14)
    ax.yaxis.grid(True, linestyle='-.')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.rcParams.update({'font.size': 15})

    legend = ax.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",  borderaxespad=0, ncol=3, handlelength=2, handletextpad=0.3, columnspacing=1, borderpad=0.3, prop={"family": "Times New Roman", "size": 24.5})
    # plt.fill_between(x, y1=0, y2=cw_dir[project], facecolor='lightskyblue', alpha=0.3)
    # plt.fill_between(x, y1=cw_dir[project], y2=se_dir[project], facecolor='lightskyblue', alpha=0.3)
    fig.savefig(target_file, bbox_inches='tight')
    

    
def draw(proj, csv_file, target_folder):
    y_time, y_test = read_summary_csv(csv_file)
    time_file = os.path.join(target_folder, "{}_time.pdf".format(proj))
    test_file = os.path.join(target_folder, "{}_test.pdf".format(proj))
    draw_helper("time", time_file, y_time)
    draw_helper("num", test_file, y_test)
    


if __name__ == '__main__':
    proj = sys.argv[1]
    csv_file = sys.argv[2] #"csv_files/hcommon/summary.csv"
    target_folder = sys.argv[3] #"figures/hcommon"
    draw(proj, csv_file,target_folder)
         

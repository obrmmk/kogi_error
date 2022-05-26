import json
import pandas as pd
from numpy import NaN
import sys
import subprocess

FILE_NAME=sys.argv[1]
datetime_info=FILE_NAME[:-5]
# PATH=f'log/{datetime_info}/'
PATH=''

# def subpro(command):
#     proc = subprocess.Popen(command)
#     proc.communicate()

def gen_errordf():
    df = pd.read_json(PATH+FILE_NAME)
    df_error = pd.concat([df[df['type']=='error'], df[df['type']=='exception_hook']])
    df_error = df_error.loc[:,['date','type','error_type','code','error','traceback','emsg']]
    df_error = df_error[df_error['error_type'].isnull() == True].dropna(subset = ['code']).drop('type',axis=1) #seq, date, type("exception_hook"), code, traceback, emsg
    list_line=[]
    for i in df_error['traceback']:
        try:
            list_line.append(i[0]['line'][:-1])
        except:
            list_line.append(NaN)
    df_error['line']=list_line
    df_error = df_error.dropna(subset = ['line'])
    return df_error

def line_emsg(df_error):
    df_line_emsg = df_error.loc[:,['date', 'line', 'emsg']].sort_values('date')
    return df_line_emsg 

def date_line_emsg(df_line_emsg):
    df_date_line_emsg= df_line_emsg.reset_index().drop('index',axis=1)
    df_date_line_emsg.to_csv(PATH+f'{datetime_info}_date_line_emsg.csv', index=True)

def line_emsg_drop(df_line_emsg):
    df_line_emsg_drop = df_line_emsg.drop_duplicates(subset='emsg')
    df_line_emsg_drop = df_line_emsg_drop.loc[:,['line', 'emsg']].reset_index().drop('index',axis=1)
    df_line_emsg_drop.to_csv(PATH+f'{datetime_info}_line_emsg.csv', index=True)

def freq(df_line_emsg):
    df_freq = pd.DataFrame(df_line_emsg.value_counts('emsg')).reset_index().set_axis(['emsg', 'freq'], axis=1)
    df_freq.to_csv(PATH+f'{datetime_info}_freq_emsg.csv')

def main():
    
    # subpro(['mkdir', f'log/{datetime_info}'])
    # subpro(['mv', FILE_NAME, PATH])

    df_line_emsg = line_emsg(gen_errordf())
    date_line_emsg(df_line_emsg)
    line_emsg_drop(df_line_emsg)
    freq(df_line_emsg)

main()

import gradio as gr
import pandas as pd

def special_split(file_csv):
    '''Read the file'''
    full_file = pd.read_csv(file_csv)
    full_file['active_mobile_score'] = full_file['active_mobile_score'].astype(float)
    full_file.drop_duplicates(subset=['mobile'])
    
    '''Unmatched and Matched files'''
    unmatched_file = full_file[full_file.drop(columns=full_file.columns[5]).isnull().all(axis=1) & full_file.iloc[:, 5].notnull()]
    matched_file = full_file[~full_file.index.isin(unmatched_file.index)]
    
    '''Establishing the numbered files'''
    zero_to_one = matched_file[matched_file['active_mobile_score'] >= 0]
    zero_to_one = zero_to_one[zero_to_one['active_mobile_score'] < 1]
    
    one_to_five = matched_file[matched_file['active_mobile_score'] >= 1]
    one_to_five = one_to_five[one_to_five['active_mobile_score'] < 5]
    
    five_to_ten = matched_file[matched_file['active_mobile_score'] >= 5]
    five_to_ten = five_to_ten[five_to_ten['active_mobile_score'] < 10]

    ten = matched_file[matched_file['active_mobile_score'] == 10]

    '''Save files'''
    zero_to_one.to_csv('zero_to_one.csv')
    one_to_five.to_csv('one_to_five.csv')
    five_to_ten.to_csv('five_to_ten.csv')
    ten.to_csv('ten.csv')
    unmatched_file.to_csv('unmatched.csv')
    matched_file.to_csv('matched.csv')

    
    return 'zero_to_one.csv', 'one_to_five.csv', 'five_to_ten.csv', 'ten.csv', 'unmatched.csv', 'matched.csv'
 
    

interface = gr.Interface(
    fn=special_split,
    inputs=gr.File(label="Upload CSV File"),
    outputs=[gr.File(label="Zero to One"), gr.File(label="One to Five"), gr.File(label="Five to Ten"), gr.File(label="Ten"), gr.File(label="Unmatched"), gr.File(label="Matched")]
)

interface.launch()

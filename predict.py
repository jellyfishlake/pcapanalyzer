import sys, argparse, os
import pandas as pd
import jinja2
from pycaret.classification import *
from pycaret.datasets import get_data
from datetime import datetime
from datetime import date
from xhtml2pdf import pisa




def pcap_to_predict(arguments):

        try:
            os.system("sh preprocess_pcap.sh " + arguments['argpcap'])
            df = pd.read_json("./data.json")
        except:
            print("An error occurred. Please check the documentation")
            

        # Checks for mode Argument and 
        if arguments['argmode'] == "0":
            dftmp = df[(df['dstPortClass'] == "http") | (df['dstPortClass'] == "https")]
            mode = "HTTP(S) only"
        if arguments['argmode'] == "1":
            dftmp = df[(df['l4Proto'] == 6) | (df['l4Proto'] == 17)]
            mode = "TCP/UDP"
        
        
        # TODO: Cleanup, ff
        httphosts = dftmp['httpHosts'].value_counts()
        sslserver = dftmp['sslServerName'].value_counts()
        flows = dftmp
        
        # Drop uneeded columns
        dftmp = dftmp.drop(['timeFirst', 'timeLast', 'dstPortClass', 'srcIP','dstIP', 'l4Proto', 'httpHosts', 'httpMimes', 'httpUsrAg', 'dnsAname', 'sslServerName'], axis=1)
        
        # Here comes the prediction
        model = load_model(arguments['argmodel'])
        predictions = predict_model(model, data = dftmp)
        preds = predictions['Label'].value_counts()
        flows['Label'] = predictions['Label']
        flows['Score'] = predictions['Score']

        return preds, httphosts, sslserver, predictions, flows, mode


def get_reportdata(preds, httphosts, sslserver, scores, flows, arguments, mode):
    start=datetime.now()
    #date = start.strftime("%m%d%Y_%H%M%S")
    time = start.strftime("%H:%M:%S")
    date = start.strftime("%m-%d-%Y")
    
    reportdata = {'pcap': arguments['argpcap'],
                  'date': str(date),
                  'time': str(time), 
                  'mode': mode, 
                  'total': (preds[0]+preds[1]), 
                  'malflows': preds[1], 
                  'benflows': preds[0],
                  'mal0010': scores[(scores['Label'] == 1) & (scores['Score'] > 0.0) & (scores['Score'] < 0.1)].shape[0],
                  'mal1020': scores[(scores['Label'] == 1) & (scores['Score'] > 0.1) & (scores['Score'] < 0.2)].shape[0],
                  'mal2030': scores[(scores['Label'] == 1) & (scores['Score'] > 0.2) & (scores['Score'] < 0.3)].shape[0],
                  'mal3040': scores[(scores['Label'] == 1) & (scores['Score'] > 0.3) & (scores['Score'] < 0.4)].shape[0],
                  'mal4050': scores[(scores['Label'] == 1) & (scores['Score'] > 0.4) & (scores['Score'] < 0.5)].shape[0],
                  'mal5060': scores[(scores['Label'] == 1) & (scores['Score'] > 0.5) & (scores['Score'] < 0.6)].shape[0],
                  'mal6070': scores[(scores['Label'] == 1) & (scores['Score'] > 0.6) & (scores['Score'] < 0.7)].shape[0],
                  'mal7080': scores[(scores['Label'] == 1) & (scores['Score'] > 0.7) & (scores['Score'] < 0.8)].shape[0],
                  'mal8090': scores[(scores['Label'] == 1) & (scores['Score'] > 0.8) & (scores['Score'] < 0.9)].shape[0],
                  'mal9010': scores[(scores['Label'] == 1) & (scores['Score'] > 0.9) & (scores['Score'] < 1.0)].shape[0],
                  'ben0010': scores[(scores['Label'] == 0) & (scores['Score'] > 0.0) & (scores['Score'] < 0.1)].shape[0],
                  'ben1020': scores[(scores['Label'] == 0) & (scores['Score'] > 0.1) & (scores['Score'] < 0.2)].shape[0],
                  'ben2030': scores[(scores['Label'] == 0) & (scores['Score'] > 0.2) & (scores['Score'] < 0.3)].shape[0],
                  'ben3040': scores[(scores['Label'] == 0) & (scores['Score'] > 0.3) & (scores['Score'] < 0.4)].shape[0],
                  'ben4050': scores[(scores['Label'] == 0) & (scores['Score'] > 0.4) & (scores['Score'] < 0.5)].shape[0],
                  'ben5060': scores[(scores['Label'] == 0) & (scores['Score'] > 0.5) & (scores['Score'] < 0.6)].shape[0],
                  'ben6070': scores[(scores['Label'] == 0) & (scores['Score'] > 0.6) & (scores['Score'] < 0.7)].shape[0],
                  'ben7080': scores[(scores['Label'] == 0) & (scores['Score'] > 0.7) & (scores['Score'] < 0.8)].shape[0],
                  'ben8090': scores[(scores['Label'] == 0) & (scores['Score'] > 0.8) & (scores['Score'] < 0.9)].shape[0],
                  'ben9010': scores[(scores['Label'] == 0) & (scores['Score'] > 0.9) & (scores['Score'] < 1.0)].shape[0],
                  'rigek': scores[(scores['Label'] == 2)].shape[0],
                  'trickbot': scores[(scores['Label'] == 3)].shape[0],
                  'cobaltstrike': scores[(scores['Label'] == 4)].shape[0],
                  'httphost': flows['httpHosts'][(flows['Label'] == 1)].value_counts()}
  
    return reportdata



def get_reporting(reportdata, df, a, flows, multiclass_flows):
        
        # Create Jinja Environment
	html = jinja2.Environment(
        	loader=jinja2.FileSystemLoader(searchpath='')).get_template(
        	'report_template.html').render(date=date.today().strftime('%d, %b %Y'),datetime=datetime.now().strftime('%H:%M:%S'),reportdata=reportdata, df=[df,a, flows, multiclass_flows])
	
	# Convert HTML to PDF
	with open('report_%s.pdf' % str(date.today().strftime('%m-%d-%Y')), "w+b") as out_pdf_file_handle:
		pisa.CreatePDF(
		    src=html,  # HTML to convert
		    dest=out_pdf_file_handle)  # File handle to receive result
		    
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        help="Provide name of trained model file (.pkl) but without '.pkl' extension name")
    parser.add_argument(
        "--pcap",
        help="Provide path to packet capture on which to make predictions.")
    parser.add_argument(
        "--mode",
        help="Provide mode, either (0|1). 0 stands for HTTP(S) flow predictions and 1 for TCP/UDP flow prediction.")
    args = parser.parse_args()
    
    arguments = { 'argpcap': str(args.pcap), 'argmodel': args.model, 'argmode': str(args.mode)}
    
    # pcap to predict returns reporting data in dataframes
    preds, httphosts, sslserver, scores, flows, mode = pcap_to_predict(arguments)
    
    # function to extract results from dataframes. Returns an dictionary
    reportdata = get_reportdata(preds, httphosts, sslserver, scores, flows, arguments, mode)

    # create report and save it into the same directory 
    df = flows[['srcIP','dstIP','srcPort','dstPort','l4Proto','Label','Score']].copy()
    
    df_multiclass = df[(df['Label'] == 2) | (df['Label'] == 3) | (df['Label'] == 4)]
    df_multiclass = df_multiclass.sort_values(by='Score', ascending=False)
    get_reporting(reportdata,httphosts, sslserver, df, df_multiclass)

 
    
if __name__ == '__main__':
    main(sys.argv)

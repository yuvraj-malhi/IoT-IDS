# -*- coding: utf-8 -*-
"""Decision_Tree_Edge_Test.ipynb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SotiehBOX4VVTeUXoyUCnB_0fyjvUkVa
"""

from google.colab import drive
drive.mount('/content/drive')

model = "Decision_Tree"
from sklearn.tree       import DecisionTreeClassifier;

import pickle;
import sys;
import shelve;
import warnings;
import time;
warnings.filterwarnings('ignore')
import matplotlib.patches as mpatches
import pandas             as pd;
import numpy              as np;
import seaborn            as sns;
import matplotlib.pyplot  as plt;
from sklearn.compose          import make_column_transformer
from sklearn.preprocessing    import OneHotEncoder, StandardScaler
from sklearn.model_selection  import train_test_split
from sklearn.metrics          import confusion_matrix, accuracy_score, f1_score, classification_report,precision_score, recall_score
from sklearn.utils            import resample
from imblearn.over_sampling   import SMOTENC


########################## Part 1 Data Preprocessing ##########################
print("\nPART 1 Start: Data preprocessing...")

############ Reading File ############
print("\t> Reading file...")
sh_file   = '/content/drive/MyDrive/Data/shelf_edge_DT'
data_path = '/content/drive/MyDrive/Data/kddcup.data.corrected'

df        = pd.read_csv(data_path, header=None);

for i in range(42):                                       # Rename columns
  df.rename(columns = {i: str(i)}, inplace = True) 

pehele = df['41'].value_counts()


############ Combining smaller categories ############
print("\t> Extracting smaller and minimal categories...")

tmp = pd.DataFrame();
df2 = pd.DataFrame();

few = ['spy.','perl.','phf.','multihop.','ftp_write.','loadmodule.','rootkit.','imap.','warezmaster.','land.','buffer_overflow.','guess_passwd.','pod.']
for fff in few:
  tmp = df.loc[df['41'] == fff];
  df2 = pd.concat([df2,tmp]);
  df.drop(df[df['41'] == fff].index ,inplace=True);    


########### SMOTE Smaller categories ###############
print("\t> Synthetically generating new smaller categories...")


td = df.loc[df['41'] == 'normal.'];
td = resample(td, replace=False, n_samples=450, random_state=1);   ##### C point - size of smaller sample smotes

for i in range(42):                                      
  df2.rename(columns = {i: str(i)}, inplace = True);

few = ['multihop.','ftp_write.','loadmodule.','rootkit.','imap.','warezmaster.','land.','buffer_overflow.','guess_passwd.','pod.'];
smotenc = SMOTENC([1,2,3,6,11,20,21], random_state=1);

for smaller in few:
  tt = df2.loc[df2['41'] == smaller];
  df_tmp = pd.concat([tt,td]);

  X_tmp  = df_tmp.iloc[:,:-1];
  Y_tmp  = np.array(df_tmp.iloc[:,-1]);
  Y_tmp  = Y_tmp.reshape(len(Y_tmp),1);

  X_tmpo ,Y_tmpo = smotenc.fit_resample(X_tmp,Y_tmp);

  X_tmpo = pd.DataFrame(X_tmpo);
  Y_tmpo = pd.DataFrame(Y_tmpo);
  X_tmpo.rename(columns={'0':'123'});

  if smaller == few[0]:
    X_tmt = X_tmpo;
    Y_tmt = Y_tmpo;
  else:
    X_tmt = pd.concat([X_tmt,X_tmpo]); 
    Y_tmt = pd.concat([Y_tmt,Y_tmpo]); 


df_synthesised = pd.DataFrame(np.concatenate((X_tmt,Y_tmt), axis=1));
df_synthesised.drop(df_synthesised[df_synthesised[41] == 'normal.'].index ,inplace=True);

for i in range(42):                                    
  df_synthesised.rename(columns = {i: str(i)}, inplace = True);

df = pd.concat([df,df_synthesised]);


########### SMOTE Minimal categories ###############
print("\t> Synthetically generating new minimal categories...")

td = df.loc[df['41'] == 'normal.'];
td = resample(td, replace=False, n_samples=250, random_state=1);              ##### C point - size of really small smotes

few = ['spy.','perl.','phf.'];
smotenc = SMOTENC([1,2,3], random_state=1);

for smaller in few:
  tt     = df2.loc[df2['41'] == smaller];
  tt     = resample(tt, replace=True, n_samples=10, random_state=1);
  df_tmp = pd.concat([tt,td]);

  X_tmp  = df_tmp.iloc[:,:-1];
  Y_tmp  = np.array(df_tmp.iloc[:,-1]);
  Y_tmp  = Y_tmp.reshape(len(Y_tmp),1);

  X_tmpo ,Y_tmpo = smotenc.fit_resample(X_tmp,Y_tmp);

  X_tmpo = pd.DataFrame(X_tmpo);
  Y_tmpo = pd.DataFrame(Y_tmpo);
  X_tmpo.rename(columns={'0':'123'});

  if smaller == few[0]:
    X_tmt = X_tmpo;
    Y_tmt = Y_tmpo;
  else:
    X_tmt = pd.concat([X_tmt,X_tmpo]); 
    Y_tmt = pd.concat([Y_tmt,Y_tmpo]); 


dft = pd.DataFrame(np.concatenate((X_tmt,Y_tmt), axis=1));
dft.drop(dft[dft[41] == 'normal.'].index ,inplace=True);

for i in range(42):                                     
  dft.rename(columns = {i: str(i)}, inplace = True);

df_synthesised = pd.concat([df_synthesised, dft]);


########### Oversampling ###########
print("\t> Oversampling smaller and minimal categories...")

df_oversampled = resample(df_synthesised, replace=True, n_samples=5000, random_state=1);  ###### C Point - Oversampling weight
df_synthesised = pd.concat([df_synthesised,df_oversampled]);


############ Down Sampling ############
print("\t> Down Sampling the normal class and enormous categories of attack class...")

df_down = df;

for str1 in ['normal.','smurf.', 'neptune.']:
  new = df_down.loc[df_down['41']==str1]
  if str1 == 'normal.':
    new = new.sample(n=150000, replace=False, random_state=1 );
  else:
    new = new.sample(n=150000, replace=False, random_state=1 );
  df_down.drop(df_down[df_down['41']==str1].index ,inplace=True)
  df_down = pd.concat([new, df_down]);

df_finalsample = pd.concat([df_down,df_synthesised]);
beechka = df_finalsample['41'].value_counts();


############ Combining ############
print("\t> Comining all preprocessed data into dataframe...")

dfnormal = df_finalsample.loc[df_finalsample['41']=='normal.']
dfattack = df_finalsample.loc[df_finalsample['41']!='normal.']
dfattack['41'] = 'attack.'

df = pd.concat([dfnormal,dfattack]);
baadka = df['41'].value_counts();



########################## Part 2 Training Model ##########################
print("\nPART 2 Start: Running training routine...")


############ Getting Training data ############
print("\t> Extracting training data...")
X         = df.iloc[:,:-1];
Y         = np.array(df.iloc[:,-1]);
Y         = Y.reshape(len(Y),1)


############ Target Encoding ############
print("\t> Encoding Target...")
Y = pd.DataFrame(Y);
Y.loc[Y[0] != 'normal.',0] = 1;
Y.loc[Y[0] == 'normal.',0] = 0;
#Y[0].Weight = Y[0].Weight.astype('int64')
Y = np.array(Y);
Y  = Y.astype(float)


############ Input Encoding for columns 1,2,3 ############
print("\t> Encoding Input...")
IE = make_column_transformer((OneHotEncoder(),['1','2','3']),remainder = 'passthrough');
IE.fit(X);
X = pd.DataFrame(IE.transform(X));


############ Train test split (80%, 20% ratio) ############
print("\t> Splitting into Train and Test Data...")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1);
Y_train = Y_train.reshape(len(Y_train),1)
Y_test  = Y_test.reshape(len(Y_test),1)


############# Scaling Input #############
print("\t> Scaling Input...")
SCALE_IN  = StandardScaler();
SCALE_IN.fit(X_train);
X_train = SCALE_IN.transform(X_train);

X_test  = SCALE_IN.transform(X_test);
input_dimension = 122;            


############# Training Model #############
print("\t> "+model+": Training model...")
Y_train = Y_train.flatten();
Y_test  = Y_test.flatten();

MODEL = DecisionTreeClassifier()
MODEL.fit(X_train, Y_train)
Y_pred = MODEL.predict(X_test)

Y_pred_prob = MODEL.predict_proba(X_test);


############# Inverse Label Encoding and Results #############
print("\t> Inverse Target Encoding...")

Y_pred = Y_pred.astype('int');
Y_test = Y_test.astype('int');

Y_pred = pd.DataFrame(Y_pred);
Y_test = pd.DataFrame(Y_test);

Y_pred.loc[Y_pred[0] != 0,0] = 'attack';
Y_pred.loc[Y_pred[0] == 0,0] = 'normal';

Y_test.loc[Y_test[0] != 0,0] = 'attack';
Y_test.loc[Y_test[0] == 0,0] = 'normal';

########################## Part 3 Prediction pipleine and testing ##########################
print("\nPART 3: Testing model")

############# Prediction pipeline function #############
print("\t> Creating prediction pipeline function...")

def TEST(data):
  d = pd.DataFrame(data);
  sh = d.shape;
  if sh[1]==41:

    # Column naming
    for i in range(41):
      d.rename(columns = {i: str(i)}, inplace = True) 
    
    # Column division
    X_pred = d.iloc[:,:];

    # Encoding categorical variables
    X_pred = pd.DataFrame(IE.transform(X_pred));

    # Scaling
    X_pred = SCALE_IN.transform(X_pred);
    
    # Prediction
    Y_pred = MODEL.predict(X_pred);
    
    # Decoding
    Y_pred = pd.DataFrame(Y_pred);
    Y_pred.loc[Y_pred[0] != 0, 0] = 'attack.'
    Y_pred.loc[Y_pred[0] == 0, 0] = 'normal.'

    return pd.DataFrame(Y_pred);

  else:
    return 0;


############# Test Bench #############

print("\t> Reading file...")
df_backup        = pd.read_csv(data_path, header=None);

############# Performance Metrics #############
print("\n-------------------- MODEL TESTING for Edge Module ("+model+") --------------------------\n")
time_total    = 0;
sample_total  = 0;
time_values   = np.array([0]);
sample_values = np.array([0]);
avg_speed     = np.array([0]);
inst_speed    = np.array([0]);

f1t = 0;
act = 0;
ac_values = np.array([0]);
f1_values = np.array([0]);

for rx in range(25):
  finalT = pd.DataFrame(df_backup.sample(n=40000, replace=False, random_state=rx+1 ))

  X_finalT = pd.DataFrame(finalT.iloc[:,:-1]);
  Y_finalT = pd.DataFrame(finalT.iloc[:,-1]);
  Y_finalT.loc[Y_finalT[41] != 'normal.',41] = 'attack.'

  t_init = time.clock();
  Y_finalP = TEST(X_finalT);                      
  t1 = time.clock() - t_init;

  s1 = 40000
  time_total   = time_total   + t1;
  sample_total = sample_total + s1;

  if rx!=25:
    time_values   = np.append(time_values,t1);
    sample_values = np.append(sample_values,s1);
    avg_speed     = np.append(avg_speed,sample_total/time_total);
    inst_speed    = np.append(inst_speed,s1/t1);

  a1 = accuracy_score(Y_finalT,Y_finalP)
  f1 = f1_score(Y_finalT,Y_finalP, average='macro')
  act = act + a1;
  f1t = f1t + f1;
  ac_values =np.append(ac_values,a1);
  f1_values =np.append(f1_values,f1);

f1t = f1t/25;
act = act/25;
p = pickle.dumps(MODEL)
size = sys.getsizeof(p)
unit = "b"

if size > 1000000:
  size = size/1000000
  unit = "mb"

elif size > 1000:
  size = size/1000
  unit = "kb"


print("\t Test Model F1 Score - "+str(f1t));
print("\t Test Model Accuracy - "+str(act));
print("\t Test Model Speed    - "+str(avg_speed[25])+" packets/sec");
print("\t Test Model Size     - "+str(size)+" "+unit);
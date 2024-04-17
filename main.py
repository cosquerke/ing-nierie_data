# Auteurs: COSQUER Kévin - LARTIGUE Arnaud
# Imports
import pandas as pd

# Variables globales
client_df_brut = pd.read_csv("X.csv", delimiter=",")
batiment_df_brut = pd.read_csv("Y.csv", delimiter=",")
full_df_brut = pd.merge(client_df_brut, batiment_df_brut, on='Identifiant')  ### Fusion des deux df car ils disposent d'un dénominateur commun: l'identifiant du contrat. Les dataframes ont le même nombre de ligne (10229)
clean_df = None
# Fonctions

# main
# Etape n°1: nettoyage du dataframe
# Suppression des colonnes indiquant le numero de la ligne
clean_df = full_df_brut.drop("Unnamed: 0_x", axis=1)
clean_df = clean_df.drop("Unnamed: 0_y", axis=1)
# On se sert des identifiant pour identifier les batiments, ils sont uniques à chaque batiment
print(clean_df["Identifiant"].is_unique)

# Verification des valeurs nulles
print(clean_df.isnull().sum()) # Colonnes Insee, superficief et ft_22_categ comportent des valeurs nulles. 
percet_of_nullable_values = (clean_df["ft_22_categ"].isnull().sum() / clean_df.shape[0]) * 100 # 12% de valeur nulles pour ft_22_categ, l'analyse de cette variable semble difficle. Cependant, elle est notée comme importante, on supprime les lignes ou la valeur vaut null
clean_df = clean_df.dropna(subset=['ft_22_categ'])
#clean_df = clean_df.drop("ft_22_categ", axis=1)
### QUESTION: Interet de supprimer les lignes à valeur pour les 2 autres colonnes ?
print(clean_df[clean_df['superficief'].isna()])
nullable_lines = clean_df.loc[clean_df['superficief'].isnull() & clean_df['Insee'].isnull()]
print(nullable_lines) ### Dans la plupart des cas si le code Insee est null alors la superficie aussi, les variables sont en correlation sur ce ce point. On peut donc supprimer ces lignes

clean_df = clean_df.dropna(subset=['superficief', 'Insee'])
print(clean_df.isnull().sum()) # plus aucunes valeurs nulles

# Etape n°2: Typage des variables
print(clean_df.info())

# Transformation de la valuer cible en booleen
clean_df['target'] = clean_df['target'].astype('int64').astype(object)

# Transformation de la valuer EXPO en Flotant
clean_df['EXPO'] = clean_df['EXPO'].str.replace(',', '.').astype(float)

print(clean_df.info())
print(clean_df.head())
#print(client_df_brut.shape,batiment_df_brut.shape,full_df_brut.shape, clean_df.info())
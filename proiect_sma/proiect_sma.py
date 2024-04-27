# Proiect SMA Nicolescu Paul-Andrei
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ttest_rel

date = pd.read_csv(r"Rezultate2.csv")

# Realizarea studiului descriptiv pentru variabilele gen, domiciliu, opinia despre materie,
# numarul de ore petrecut invatand, rezultatele la examene (partial si final).

# Analiza variabilelor calitative
# Numarul de studenti in functie de gen
gen_counts = date['Genul'].value_counts()
print("Numarul de studenti în functie de gen:")
print(gen_counts)

# Vizualizam numarul de studenti in functie de gen
plt.figure(figsize=(6, 4))
gen_counts.plot.pie()
plt.ylabel('Numarul de studenti')
plt.title('Distributia studentilor în functie de gen')
plt.show()

# Numarul de studenti in functie de domiciliu
domiciliu_counts = date['Domiciliul'].value_counts()
print("\nNumarul de studenti in functie de domiciliu:")
print(domiciliu_counts)

# Vizualizam numarul de studenti in functie de domiciliu
plt.figure(figsize=(6, 4))
domiciliu_counts.plot.pie()
plt.ylabel('Numarul de studenti')
plt.title('Distributia studentilor in functie de domiciliu')
plt.show()

# Numarul de studenti in functie de opinia despre materie
opinie_counts = date['Materia este interesanta'].value_counts()
print("\nNumarul de studenti in functie de opinia despre materie:")
print(opinie_counts)

# Vizualizam numarul de studenti in functie de opinia despre materie
plt.figure(figsize=(12, 4))
opinie_counts.plot.barh()
plt.ylabel('Materia este interesanta?')
plt.xlabel('Numarul de studenti')
plt.title('Distributia studentilor in functie de opinia despre materie')
plt.show()

# Studiul descriptiv pentru numarul de ore dedicate invatarii
ore_invatare_counts = date['Ore dedicate invatarii'].value_counts()
ore_invatare_stats = date['Ore dedicate invatarii'].describe()
print("Studiu descriptiv pentru numarul de ore dedicate invatarii:")
print(ore_invatare_counts)
print(ore_invatare_stats)

# Vizualizare distributie numar de ore dedicate invatarii
plt.figure(figsize=(8, 4))
plt.hist(date['Ore dedicate invatarii'])
plt.xlabel('Numarul de ore dedicate invatarii')
plt.ylabel('Numarul de studenti')
plt.title('Distributia numarului de ore dedicate invatarii')
plt.show()

# Studiu descriptiv pentru rezultatele la examenul partial
print("\nStudiu descriptiv pentru rezultatele la examenul partial")
print("Medie examen partial: " + str(date['Examen Partial (4p)'].mean()))
print("Deviatie standard examen partial: " + str(date['Examen Partial (4p)'].std()))
print("Mediana examen partial: " + str(date['Examen Partial (4p)'].median()))
print("Minim examen partial: " + str(date['Examen Partial (4p)'].min()))
print("Maxim examen partial: " + str(date['Examen Partial (4p)'].max()))
ex_partial_cv = (date['Examen Partial (4p)'].std() / date['Examen Partial (4p)'].mean()) * 100
print("Coeficient de variatie examen partial:", ex_partial_cv)

# Vizualizare distributie rezultate examen partial
plt.figure(figsize=(8, 4))
plt.hist(date['Examen Partial (4p)'])
plt.xlabel('Rezultat examen partial')
plt.ylabel('Numarul de studenti')
plt.title('Distributia rezultatelor la examenul partial')
plt.show()

# Studiu descriptiv pentru rezultatele la examenul final
print("\nStudiu descriptiv pentru rezultatele la examenul final")
print("Medie examen final: " + str(date['Examen Final (6p)'].mean()))
print("Deviatie standard examen final: " + str(date['Examen Final (6p)'].std()))
print("Mediana examen final: " + str(date['Examen Final (6p)'].median()))
print("Minim examen final: " + str(date['Examen Final (6p)'].min()))
print("Maxim examen final: " + str(date['Examen Final (6p)'].max()))
ex_final_cv = (date['Examen Final (6p)'].std() / date['Examen Final (6p)'].mean()) * 100
print("Coeficient de variatie examen final:", ex_final_cv)

# Vizualizare distributie rezultate examen final
plt.figure(figsize=(8, 4))
plt.hist(date['Examen Final (6p)'])
plt.xlabel('Rezultat examen final')
plt.ylabel('Numarul de studenti')
plt.title('Distributia rezultatelor la examenul final')
plt.show()

# Calcularea si interpretarea coeficientului de corelatie dintre rezultatele partiale si
# finale ale studentilor.
coef_corelatie = date['Examen Partial (4p)'].corr(date['Examen Final (6p)'])
print("\nCoeficientul de corelatie intre rezultatele partiale si finale:", coef_corelatie)
print("Exista o corelatie pozitiva moderata intre rezultatele partiale si finale(0.4 < coef_corelatie < 0.6).")

# Verificarea existentei unor diferente semnificative intre rezultatele totale (final+partial)
# obtinute de fete si rezultatele totale (final+partial) obtinute de baieti.
# Filtram datele pentru fete si baieti
rezultate_fete = date[date['Genul'] == 'F']['Total (10p)']
rezultate_baieti = date[date['Genul'] == 'B']['Total (10p)']
# Efectuam Independent Sample T-test
rezultat_ttest, pvalue = ttest_ind(rezultate_fete, rezultate_baieti, equal_var=True)
print("\nRezultat test t:", rezultat_ttest)
print("p-value:", pvalue)
print("Deoarece p-value > 0.05, acceptam ipoteza de nul, adica nu exista o diferenta")
print("semnificativa intre rezultatele totale obtinute de fete si baieti.")

# Verificarea existentei unor diferente semnificative intre rezultatele (final+partial)
# obtinute de studenti in functie de domiciliu.
# Filtram datele pentru urban si rural
rezultate_urban = date[date['Domiciliul'] == 'urban']['Total (10p)']
rezultate_rural = date[date['Domiciliul'] == 'rural']['Total (10p)']
# Efectuam Independent Sample T-test
rezultat_ttest2, pvalue2 = ttest_ind(rezultate_urban, rezultate_rural, equal_var=True)
print("\nRezultat test t 2:", rezultat_ttest2)
print("p-value 2:", pvalue2)
print("Deoarece p-value < 0.05, respingem ipoteza de nul, adica exista suficiente")
print("informatii pentru a putea spune ca exista o diferenta statistica a rezultatului")
print("total, pe baza domiciliului")

# Rescalarea rezultatelor de la examenul partial si examenul final astfel incat sa fie
# ambele din 10p. Verificam daca exista diferente semnificative intre rezultatele
# studentilor la cele doua examene.
# Redimensionam rezultatele de la examenul partial si final
ex_partial_rescal = (date['Examen Partial (4p)'] * 2.5)
ex_final_rescal = (date['Examen Final (6p)'] * (10/6))
# Efectuam Paired t-test
rezultat_ttest3, pvalue3 = ttest_rel(ex_partial_rescal, ex_final_rescal)
print("\nRezultat test t 3:", rezultat_ttest3)
print("p-value 3:", pvalue3)
print("Deoarece p-value > 0.05, acceptam ipoteza de nul, adica nu exista suficiente")
print("informatii pentru a putea spune ca exista o diferenta semnificativa a rezultatelor")
print("studentilor la cele doua examene")

# Popis vypracovania

Ako úlohu som si vybral problém producent-konzument. Ako kritérium optimalizačnej úlohy som si vybral počet vyrobených výrobkov za jednotku času Pre každý z parametrov som generoval 110-krát náhodné číslo v rozsahu 1-15. Program som nechal bežať 60 sekúnd a zapísal som si, koľko sa vyprodukovalo a spotrebovalo pre danú kombináciu parametrov. Toto som zopakoval 10x a výsledné hodnoty spriemeroval. Hodnoty som následne zapísal do csv súboru, aby som pri vytváraní grafov nemusel vždy čakat na zbehnutie celého programu.


Ďalej som si vytvoril grafy a pozeral som ako spolu súvisia jednotlivé parametre. Ako najoptimálnejšia kombinácia pri vygenerovaných náhodných číslach pri ktorej sa vyprodukovalo 402 kusov za minútu mi vyšla:
1. producers - 15
2. consumers - 13
3. production time - 1
4. consumption time - 2
5. capacity - 12


Najlepšie výsledky mali očakávane kombinácie, kde bol nízky čas produkcie aj konzumácie a vysoký počet producentov a konzumentov. Dôležitý bol aj pomer producentov a konzumentov, a ich časov. Najlepšie boli pomery blízko ku 1:1. Je to z toho dôvodu, že ak je medzi nimi nepomer, tak sa buď naplní kapacita, alebo konzumenti musia dlhšie čakať na výrobu
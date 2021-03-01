# Otázky zo zadania
## 1) Aký je najmenší počet synchronizačných objektov (semafory, mutexy, udalosti) potrebných na riešenie tejto úlohy?

Najmenší počet potrebných synchronizačných objektov je rovný počtu vlákien. V mojom riešení som použil o dva semafory/udalosti viac pre zjednodušenie kódu, ale semafory/udalosti pre prvý a druhý prvok fibonacciho postupnosti by sa dali odstrániť.

## 2) Ktoré z prebratých synchronizačných vzorov (vzájomné vylúčenie, signalizácia, rendezvous, bariéra) sa dajú (rozumne) využiť pri riešení tejto úlohy? Konkrétne popíšte, ako sa ten-ktorý synchronizačný vzor využíva vo vašom riešení.

- **vzájomné vylúčenie** - pri tomto zadaní nestačí keďže sa poradie v akom idú vlákna môže meniť a niektoré vlákno by mohlo pri výpočte používať hodnotu, ktorá ešte nebola vypočítaná
- **signalizácia** - v tomto zadaní som ju použil tak, že som signalizoval čakajúcemu vláknu keď sa vypočítala hodnota ktorú potrebuje na svoj vlastný výpočet
- **rendezvous** - nie je potrebná, lebo nechceme aby vlákna na seba obojstranne čakali
- **bariéra** - nie je potrebná z rovnakého dôvodu ako rendezvous
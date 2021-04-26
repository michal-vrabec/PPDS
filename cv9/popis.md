# Popis

Python script konvertuje obrázok v RBG na greyscale. Počíta hodnoty pixelov najprv sekvenčne na CPU a potom pomocou CUDA kernelu. Následne vypíše rýchlosti jednotlivých typov výpočtu a uloží greyscale obrázok do súboru "output.jpg".
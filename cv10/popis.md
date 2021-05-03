# Popis

Minulotýždňové zadanie som prerobil, aby paralelne transformovalo 10 obrázkov do greyscale pomocou streamov. Čas výpočtov pre jednotlivé obrázky som ukladal pomocou udalostí. Po použití occupancy calculatora a taktiež skúšania rôznych kombinácií parametrov bol najrýchlejší výpočet s 64 threads per block.
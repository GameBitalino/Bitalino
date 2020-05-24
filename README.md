Terapeutická hra pro měření reakční doby s využitím platformy BITalino

Hra:
Úkolem je ovládat hru kontrakcí a dilatací svalu, a co nejrychleji reagovat na generované podněty - změna barvy semaforu, zobrazení vozu záchranné služby.

Cílem hry je zároveň dosáhnout co nejvyššího skóre. Čím delší vzdálenost ve hře hráč urazí, tím vyšší skóre získá. V případě, že hráč reaguje na podněty dostatečně rychle, získává „bonusy“, což navýší celkové skóre. Obdobně je to v případě sbírání hvězdiček. 
S ujetou vzdáleností ubývá paliva, které hráč doplní tak, že střetne ikonu reprezentující benzín. 
V průběhu hry se protijedoucí vozidla pohybují čím dál rychleji, což zvyšuje obtížnost hry. 

Příprava hry: 
Umístění elektrod: na dolní končetině podle doporučení SENIAM, kdy pro měření aktivity svalu gastrocnemius lateralis má být aktivní elektroda umístěna v jedné třetině mezi hlavou fibuly a patou
Zapojeníé zařízení BITalino a zapnuté bluetooth
Snímání a správnost zapojení BITalina je možno oveřit spuštěním skriptu "real_time_plot_BITalino_measurement.py"
Další potřeby: židle a pedál


Parametry: 
MAC adresa zařízení
Vzorkovací frekvence
Velikost okna, ve kterém jsou načítány signály z BITalina


Před spuštěním:
- nastavení cest
- instalace knihoven 
- úprava v knihovně "bitalino": je nutné přidat atribut do kontuktoru 
	- self.startTime = None
	- ve funkci "send" následně přidat za time.sleep(): self.startTime = datetime.datetime.now()

Spuštění hry: skript "run.py"

Nastavení ve hře:
- možnost výběru metody, jakou bude zpravováván EMG signál


Ovládání hry:

Zastavení a znovu rozjetí automobilu: sešlápnutí pedálu (využití pouze jednoho pedálu)
Pohyb doprava/doleva: šipky na klávesnici


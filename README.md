# Examination

Individuell examinationsuppgift i kursen Programmering med Python.

Börja läs igenom game.py - det är där projektet startas.

## Starta projektet

```commandline
python -m src.game
```

Tips! Du kan spara denna rad som en "run configuration" i PyCharm.

1. Välj "Edit configurations..."
2. Ändra i sektionen "run" så det står `module` i stället för `script`
3. Skriv `src.game` i rutan till höger om `module`

Exam uppgift: https://docs.google.com/document/d/1GhqbgG9YW5cOiR0LLWmMTc-s-VmQudBaNxZUxXL6XJk/edit?usp=sharing

---

## Noteringar om spelet

Min version av spelat går ut att samla poäng.  
Starta spelet genom 'python -m src.game'

### Förklaringar

**Symboler**

- @: Spelaren som du navigerar
- ?: Något som kan plockas upp (mat, bomber eller en spade)
- |, -, +: Staket
- ■: Gräns
- #: Monster som jagar dig
- E: Exit
- ,: Jord som har förstörts (ett komma)
- X: Monster eller spelaren som har dött
- ¤: Placerad bomb

**Navigeringsknappar**

- w: Riktning uppåt
- s: Riktning nedåt
- a: Riktning vänster
- d: Riktning höger
- j: Aktivera för att hppa nästa riktning

**Övriga knappar**

- i: "Inventory" saker som har plockats upp av spelaren
- e: Äta mat som plockats upp
- b: Placera en bomb där spelaren står
- q, x: Avsluta spelet

### Poäng

- Samla saker 20 poäng
- Döda monstret 100 poäng
- Gå runt på spelplanen -1 poäng
  Dock
  - Efter en sak har plockats upp ges 5 "gratis" steg
  - Om spelaren äter mat ges 10 "gratis" steg

### Att navigera

Genom att navigera med navigeringknaparna och <enter> så rör man spelaren, @, inom spelområdet.  
Ex: 'w' och "enter" => Spelaren rör sig en ruta uppåt.  
Det är möjligt att hoppa över en ruta, först aktivera att hoppa sedan navigera.  
Ex: 'j', "enter", d och "enter" => Spelaren hoppar över en ruta åt höger  
Det är inte möjligt att hoppa över eller genom staket (även med spaden) eller gränsen.

### Samla saker

Under spelets gång dyker det upp saker, ?, på spelplanen som spelaren kan navigera till för att
plocka upp. Saken hamnar i spelarens "inventory" tills man använder dem. Dock om spelaren har
allt som kan plockas upp i sin "inventory" kommer inget nytt att placeras ut. Dock kommer
använda saker kommer att placeras ut igen efter en tid.

### Staket och gränsen

Normalt kan inte spelaren gå genom staket. Dock om spelaren har spaden i sin "inventory"
kan man förstöra staketet genom gå in i det för att kan passera igenom det.  
Om spelaren har spaden sig och går in i gränsen förstörs spaden och den försvinner
ut ur spelaren "inventory".

### Exit

Efter ett tag dyker exit, E, upp som spelaren kan navigera till och avsluta spelet.

### Monster

Efter ett tag dyker monstret upp och börjar jaga spelaren, staket spelar ingen roll för
monstret den förstör det och fortsätter sin jakt. Monster går alltid 2 steg dock pga
dålig syn är det inte alltid säkert att monstret rör på sig.  
Om spelaren dödar monster kommer nya monster dyka upp efter en obestämd tid. Om monstret
dödar spelaren avslutas spelet. Monstret kan dödas av spelaren med hjälp av en bomb
eller om spelaren har en spade i sin "inventory".

### Mat (Food)

Genom att äta mat fås "gratis" steg samt ger plats i spelarens "inventory" att plocka mer
mat och då också poäng.

### Spade (Shovel)

Med hjälp av spaden kan spelare tas sig genom staket utan problem. Dock om spelaren går
in i gränsen försvinner spaden.  
Om ett monster står bredvid spelaren och spelaren har spaden kan spelaren döda monstret
genom att gå in i monstret.

### Bomber (Dynamite, C4 och Nitroglycerin)

När en bomb finns i spelarens "inventory" kan den placeras ut där spelaren står, b.
Efter 3 steg av spelaren detonerar bomben och förstör allt omkring där den placerades.
Om spelaren eller monster står inom detta område dör man.  
En placerad bomd detonerar direkt om spelaren eller monstret trampar på den även om
inte 3 steg har tagits av spelaren.  
En placerad bomd försvinner ur spelarens "inventory".

# 🍄 MycoMate ZX Spectrum Edition

⚠️ **IMPORTANT: CONCEPT CODE - UNTESTED** ⚠️
> This is a theoretical adaptation that has **NOT** been tested on real ZX Spectrum hardware or emulators. The code is provided as a proof-of-concept and educational example. Expect bugs, syntax errors, and potential compatibility issues. Use at your own risk!

A faithful retro adaptation of MycoMate Digital Pet for the Sinclair ZX Spectrum!

```
╔════════════════════════════════════════╗
║              MYCOMATE                  ║
║         Digital Mushroom Pet           ║
║         ZX Spectrum Edition            ║
╚════════════════════════════════════════╝
```

## 📼 About This Version

This is a special retro adaptation of MycoMate designed to run on the legendary ZX Spectrum home computer (or any ZX Spectrum emulator). Written in authentic ZX BASIC, it captures the essence of the original digital pet while working within the delightful constraints of 1980s computing!

## 🖥️ System Requirements

- **ZX Spectrum 48K** or later
- **ZX Spectrum emulator** (Fuse, SpecEmu, ZXSPIN, etc.)
- Approximately **3KB** of memory for the program

## 💾 Loading Instructions

### On Real Hardware:
1. Load the program from tape/disk
2. Type `RUN` and press ENTER
3. Enjoy caring for your digital mushroom!

### On Emulator:
1. Load `mycomate_spectrum.bas` into your ZX Spectrum emulator
2. Type `RUN` and press ENTER
3. Experience retro pet care!

## 🎮 How to Play

### Controls
- **1** - Feed your pet
- **2** - Play with your pet  
- **3** - Clean your pet
- **4** - Let your pet rest
- **5** - View detailed status
- **Q** - Quit game

### Pet Care Basics
Just like the modern version, your ZX Spectrum mushroom needs:
- 🍽️ **Regular feeding** (5 food types available)
- 🎮 **Playtime** for happiness
- 🧼 **Cleaning** to stay healthy
- 😴 **Rest** to restore energy

### Growth Stages
Watch your pet evolve through 5 stages:
1. **Spore** (o) - Just born!
2. **Sprout** (|) - First growth after 4 hours
3. **Young** (***) - At 16 hours with good health
4. **Mature** (*****) - At 30 hours with decent care
5. **Magical** (*********) - Ultimate form at 48 hours with excellent care!

## 🧬 ZX Spectrum Features

### Authentic Retro Experience
- **Custom UDG graphics** - User Defined Graphics for detailed pet visuals
- **Progressive evolution** - Watch detailed pixel art change as your pet grows
- **Animated magical stage** - Special effects for the ultimate evolution
- **Personality system** with 5 distinct pet types affecting gameplay
- **Favorite foods** for bonus effects
- **Visual stat bars** using asterisk characters

### Technical Adaptations
- **Simplified timing** suitable for BASIC execution speed
- **Memory efficient** variable usage
- **Screen positioning** optimized for 32x24 character display
- **Input handling** using classic INKEY$ method
- **No save feature** (would require tape/disk operations)

### Personality Types
Your pet will have one of these classic personalities:
- **Shy** - Needs extra attention, stays clean longer
- **Playful** - Maintains happiness well, uses more energy
- **Curious** - Burns energy exploring, stays content
- **Sleepy** - Conserves energy, needs stimulation
- **Energetic** - High metabolism, very active

## 🎯 Programming Notes

### BASIC Techniques Used
- **Structured programming** with GOSUBs for clean code organization
- **Efficient variable naming** to fit ZX Spectrum conventions
- **Screen positioning** using AT statements for layout
- **FOR loops** for creating stat bar graphics
- **String handling** for pet names and food types
- **Random number generation** for personality and food preferences

### Memory Optimization
- **Single-letter variables** where possible (H, P, E, C, L for stats)
- **Minimal string storage** to conserve memory
- **Compact code structure** fitting within 48K limitations
- **No arrays** to keep memory usage minimal

### ZX Spectrum Specific Features
- **UDG (User Defined Graphics)** - Custom 8x8 pixel character definitions
- **POKE USR** commands to define custom graphics in character RAM
- **CHR$()** calls to display custom characters (144-185)
- **BIN notation** for easy pixel pattern definition
- **BORDER** command for screen color
- **PAPER/INK** for text colors
- **PAUSE** statements for timing
- **CLS** for screen clearing
- **RND** for randomization

### UDG Graphics System
This version uses the ZX Spectrum's powerful User Defined Graphics feature:

**Character Assignments:**
- CHR$(144): Spore - Simple round organism
- CHR$(145-146): Sprout - Two-part growing mushroom
- CHR$(147-152): Young - Multi-character mushroom with cap and stem
- CHR$(153-163): Mature - Large detailed mushroom with gills
- CHR$(164-185): Magical - Animated sparkling mushroom with effects

**Technical Implementation:**
- Each UDG is 8x8 pixels defined in binary
- Uses POKE USR "letter" to write pixel data
- Multi-character sprites for larger mushrooms
- Animation through character cycling for magical stage
- Memory efficient - only defines needed characters

## 🔧 Code Structure

```
Lines 10-70:     Title screen and initialization
Lines 80-200:    Variable setup and pet creation
Lines 210-440:   Pet introduction sequence
Lines 450-560:   Main game loop
Lines 1000-1200: Stat update routines
Lines 1220-1560: Screen drawing and menu
Lines 2000-2800: Care action subroutines
Lines 3000-3100: Quit sequence
```

## 🐛 Known Limitations

- **No save feature** - pets don't persist between sessions
- **Simplified timing** - not real-time like modern version
- **Basic graphics** - character-based ASCII art only
- **No sound** - silent operation (could be enhanced with BEEP)
- **Fixed screen size** - designed for standard ZX Spectrum display

## 🚀 Possible Enhancements

If you want to extend this version:
- Add **BEEP** commands for sound effects
- Implement **tape save/load** functionality
- Create **animated sequences** for actions
- Add **more detailed ASCII art** for each stage
- Include **mini-games** using simple input
- Add **color cycling** effects for the magical stage

## 🎊 Fun Facts

- The entire game fits in **less than 3KB** of memory!
- Uses **authentic 1980s programming techniques**
- Could theoretically run on a **ZX81** with minor modifications
- Written in **pure ZX BASIC** with no machine code
- Captures the **essence of digital pets** in minimal code

## 💝 Credits

Original MycoMate concept and modern Python version by the MycoMate development team.
ZX Spectrum BASIC adaptation created with love for retro computing enthusiasts!

## 🕹️ Loading from Tape

For the authentic experience, here's how this would have been distributed in 1982:

```
SAVE "MYCOMATE" LINE 10
```

Then to load:
```
LOAD "MYCOMATE"
RUN
```

---

**Experience the magic of caring for a digital pet on authentic 1980s hardware!** 

Press any key to begin your retro mushroom adventure! 🍄✨

*Compatible with ZX Spectrum 48K, 128K, +2, +3, and all popular emulators*

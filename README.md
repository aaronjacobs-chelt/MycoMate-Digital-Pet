# 🍄 MycoMate - Digital Mushroom Pet

```
🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄
      __  __                   __  __       _       
     |  \/  |                 |  \/  |     | |      
     | \  / |_   _  ___ ___   | \  / | __ _| |_ ___ 
     | |\/| | | | |/ __/ _ \  | |\/| |/ _` | __/ _ \
     | |  | | |_| | (_| (_) | | |  | | (_| | ||  __/
     |_|  |_|\__, |\___\___/  |_|  |_|\__,_|\__\___|
              __/ |                                 
             |___/                                  
            
         Your Digital Mushroom Pet Companion
🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄✨🍄
```

A Tamagotchi-style digital pet game where you care for and nurture your very own mushroom companion!

## 🎮 Features

- **5 Growth Stages**: Watch your pet evolve from Spore → Sprout → Young → Mature → Magical Mushroom
- **Real-time Care**: Your pet needs regular feeding, playing, cleaning, and rest
- **Unique Personalities**: Each pet has its own personality (shy, playful, curious, sleepy, energetic)
- **Favorite Foods**: Every pet has preferred foods that provide bonus benefits
- **Experience System**: Gain XP through care activities to unlock the magical final stage
- **Persistent Save Data**: Your pet continues growing even when you're away
- **Beautiful ASCII Art**: Different visual representations for each growth stage and mood
- **Stats Management**: Monitor hunger, happiness, health, cleanliness, and energy

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Terminal/Command line access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aaronjacobs-chelt/MycoMate-Digital-Pet.git
cd MycoMate-Digital-Pet
```

2. Run the game:
```bash
python3 mycomate.py
```

### First Time Setup

1. Enter a name for your new mushroom pet
2. Your pet will be born as a tiny spore!
3. Learn about their personality and favorite food
4. Start caring for your new companion

## 🎯 How to Play

### Pet Care Actions

| Action | Effect | Cooldown | Notes |
|--------|--------|----------|-------|
| 🍽️ **Feed** | +Hunger, +Happiness, +Health | 30 min* | Different foods have different effects |
| 🎮 **Play** | +Happiness, +XP, -Energy | 20 min | Requires >30 energy |
| 🧼 **Clean** | +Cleanliness, +Happiness, +Health | 1 hour | Keeps your pet pristine |
| 😴 **Rest** | +Energy, +Health | None | Let your pet recharge |

*Feeding cooldown is reduced if pet is very hungry

### Food Types

- **Nutrients**: Balanced nutrition (default)
- **Compost**: Great for hunger, moderate happiness
- **Water**: Moderate hunger, good energy boost
- **Sunshine**: High happiness and energy, moderate hunger
- **Minerals**: Excellent hunger, good health boost

💡 **Tip**: Feed your pet their favorite food for bonus effects!

### Growth Stages

| Stage | Requirements | Time | Health Needed | XP Needed |
|-------|-------------|------|---------------|-----------|
| 🌱 **Spore** | Starting stage | 0 hours | - | - |
| 🌿 **Sprout** | Survival | 6 hours | Any | - |
| 🍄 **Young** | Basic care | 24 hours | >40% | - |
| 🍄🍄 **Mature** | Good care | 48 hours | >60% | - |
| ✨🍄✨ **Magical** | Excellent care | 72 hours | >80% | 500+ |

### Stats Explained

- **Hunger** (0-100%): How well-fed your pet is. Decays over time.
- **Happiness** (0-100%): Your pet's mood. Increased by playing and favorite foods.
- **Health** (0-100%): Overall wellbeing. Affected by other stats.
- **Cleanliness** (0-100%): How clean your pet is. Decays slowly over time.
- **Energy** (0-100%): Available energy for activities. Restored by resting.

## 📁 Project Structure

```
MycoMate-Digital-Pet/
├── mycomate.py          # Main game file
├── README.md            # This file
├── LICENSE              # Project license
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── docs/               # Documentation
│   ├── gameplay.md     # Detailed gameplay guide
│   ├── development.md  # Development documentation
│   └── api.md          # Code documentation
├── examples/           # Example configurations
└── assets/            # Game assets and media
```

## 🛠️ Development

### Code Structure

The main game is contained in `mycomate.py` with the following key components:

- **MushroomPet Class**: Core pet logic and state management
- **Stats System**: Real-time stat updates and decay
- **Growth System**: Age-based evolution with requirements
- **UI System**: Terminal-based interface with ASCII art
- **Save System**: JSON-based persistence

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [docs/development.md](docs/development.md) for detailed development guidelines.

## 🐛 Troubleshooting

### Common Issues

**Pet won't evolve to next stage:**
- Check that enough time has passed
- Ensure health requirements are met
- For Magical stage, verify you have 500+ XP

**Stats declining too fast:**
- This is normal! Pets need regular care
- Check back every few hours to maintain stats
- Use the rest function to restore energy

**Can't find save file:**
- Save files are stored as hidden files (`.mushroom_pet_[name].json`)
- Located in your home directory by default

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by classic Tamagotchi digital pets
- ASCII art inspired by text-based adventure games
- Built with Python's standard library for maximum compatibility

## 📊 Roadmap

### Planned Features

- [ ] Multiple pet support in single session
- [ ] Pet breeding system
- [ ] Mini-games for interaction
- [ ] Seasonal events and special foods
- [ ] Pet social interactions
- [ ] Achievement system
- [ ] Custom ASCII art themes
- [ ] Mobile app version

### Version History

- **v1.0.0**: Initial release with core pet care mechanics
- **v1.1.0**: Enhanced UI and growth system improvements
- **v1.2.0**: Experience system and stat balancing

---

## 🎮 Start Your Journey

Ready to meet your new mushroom companion? Run the game and watch your spore grow into a magnificent magical mushroom through love and care!

```bash
python3 mycomate.py
```

Happy mushroom parenting! 🍄✨


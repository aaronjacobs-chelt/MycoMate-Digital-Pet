# 🛠️ MycoMate Development Guide

## Table of Contents
- [Project Structure](#project-structure)
- [Code Architecture](#code-architecture)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Testing](#testing)
- [Release Process](#release-process)

## Project Structure

```
MycoMate-Digital-Pet/
├── mycomate.py          # Main game file
├── README.md            # Project overview
├── LICENSE              # MIT License
├── requirements.txt     # Dependencies (none currently)
├── .gitignore          # Git ignore rules
├── docs/               # Documentation
│   ├── gameplay.md     # User gameplay guide
│   ├── development.md  # This file
│   └── api.md          # Code documentation
├── examples/           # Example configurations
│   └── sample_pet.json # Example save file
└── assets/            # Game assets
    └── banner.md       # ASCII art banner
```

## Code Architecture

### Core Components

#### MushroomPet Class
The main game logic is contained in the `MushroomPet` class with the following key methods:

**Initialization**:
- `__init__(name)`: Creates new pet with random personality and favorite food
- `load_from_file()`: Loads existing pet from JSON save file
- `save_to_file()`: Saves pet state to JSON file

**Stats Management**:
- `update_stats()`: Real-time stat decay and health calculations
- `update_mood()`: Mood calculation based on average stats
- `get_age_in_hours()`: Age calculation from birth time

**Care Actions**:
- `feed(food_type)`: Feeding logic with cooldowns and food effects
- `play()`: Play interaction with energy requirements
- `clean()`: Cleaning with cooldown management
- `rest()`: Energy restoration without cooldown

**Display**:
- `get_ascii_art()`: Dynamic ASCII art based on stage and mood
- `get_stage_name()`: Human-readable growth stage names
- `get_status()`: Formatted status display

#### UI System
Terminal-based interface with:
- `draw_ui(pet)`: Main UI rendering
- `show_menu()`: Action menu display
- `show_help()`: Help system
- `clear_screen()`: Cross-platform screen clearing

### Data Models

#### Pet Stats (0-100 scale)
```python
{
    "hunger": float,        # Nutrition level
    "happiness": float,     # Mood and contentment
    "health": float,        # Overall wellbeing
    "cleanliness": float,   # Hygiene level
    "energy": float         # Available energy for activities
}
```

#### Growth System
```python
{
    "age": float,           # Hours since birth
    "growth_stage": int,    # 0-4 (Spore to Magical)
    "experience": int,      # XP points earned
    "level": int           # Pet level (future use)
}
```

#### Pet Attributes
```python
{
    "name": str,            # Pet name
    "personality": str,     # shy|playful|curious|sleepy|energetic
    "favorite_food": str,   # water|compost|sunshine|minerals|nutrients
    "mood": str            # Calculated from stats
}
```

### Save System

**File Format**: JSON
**Location**: `~/.mushroom_pet_{name}.json`
**Structure**:
```json
{
    "name": "PetName",
    "birth_time": 1234567890.123,
    "last_update": 1234567890.456,
    "hunger": 75.5,
    "happiness": 80.2,
    "health": 95.0,
    "cleanliness": 85.7,
    "energy": 60.3,
    "age": 12.5,
    "growth_stage": 2,
    "personality": "playful",
    "favorite_food": "water",
    "mood": "happy",
    "last_fed": 1234567890.123,
    "last_played": 1234567890.123,
    "last_cleaned": 1234567890.123,
    "experience": 150,
    "level": 1
}
```

## Development Setup

### Prerequisites
- Python 3.6+
- Git
- Text editor or IDE

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/MycoMate-Digital-Pet.git
cd MycoMate-Digital-Pet
```

2. **Run the game**:
```bash
python3 mycomate.py
```

3. **Make changes and test**:
```bash
# Test your changes
python3 mycomate.py

# Check for syntax errors
python3 -m py_compile mycomate.py
```

### Code Style

- **PEP 8**: Follow Python style guidelines
- **Docstrings**: Use for all classes and public methods
- **Comments**: Explain complex logic and calculations
- **Variable naming**: Use descriptive names

Example:
```python
def update_stats(self):
    """Update pet stats based on time passage"""
    current_time = time.time()
    time_passed = (current_time - self.last_update) / 3600  # in hours
    
    # Stats decay over time
    self.hunger = max(0, self.hunger - (time_passed * 5))
```

## Contributing Guidelines

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
4. **Test thoroughly**
5. **Commit with descriptive messages**:
```bash
git commit -m "Add pet breeding system with genetic traits"
```

6. **Push and create Pull Request**

### Types of Contributions

**Bug Fixes**:
- Fix stat calculation errors
- Resolve UI display issues
- Correct save/load problems

**Features**:
- New care actions
- Additional growth stages
- Mini-games
- Social features

**Documentation**:
- Improve existing docs
- Add examples
- Create tutorials

**Testing**:
- Unit tests
- Integration tests
- User experience testing

### Code Review Process

1. **Automated checks**: Code style and syntax
2. **Manual review**: Logic and design
3. **Testing**: Functionality verification
4. **Documentation**: Update docs if needed

## Testing

### Manual Testing Checklist

**Basic Functionality**:
- [ ] Pet creation works
- [ ] Save/load functions correctly
- [ ] All care actions respond properly
- [ ] Stats update correctly over time
- [ ] Growth stages trigger at right times

**Edge Cases**:
- [ ] Pet with 0% stats
- [ ] Pet with 100% stats
- [ ] Long periods between care
- [ ] Rapid repeated actions
- [ ] Invalid food types

**UI Testing**:
- [ ] Display works on different terminal sizes
- [ ] Menu navigation is intuitive
- [ ] Help system is comprehensive
- [ ] Error messages are clear

### Automated Testing (Future)

```python
# Example test structure
import unittest
from mycomate import MushroomPet

class TestMushroomPet(unittest.TestCase):
    def setUp(self):
        self.pet = MushroomPet("TestPet")
    
    def test_feeding_increases_hunger(self):
        initial_hunger = self.pet.hunger
        self.pet.feed('nutrients')
        self.assertGreater(self.pet.hunger, initial_hunger)
    
    def test_growth_stage_progression(self):
        # Test growth logic
        pass
```

## Release Process

### Version Numbering
- **Major**: Breaking changes (v2.0.0)
- **Minor**: New features (v1.1.0)
- **Patch**: Bug fixes (v1.0.1)

### Release Checklist

1. **Update version number** in code comments
2. **Update CHANGELOG.md** with new features/fixes
3. **Test thoroughly** on multiple systems
4. **Update documentation** if needed
5. **Create release tag**:
```bash
git tag -a v1.1.0 -m "Version 1.1.0: Add new features"
git push origin v1.1.0
```

6. **Create GitHub release** with notes
7. **Announce** in relevant communities

### Deployment

Currently manual deployment. Future considerations:
- Package for PyPI
- Create standalone executables
- Docker containers
- Mobile app versions

## Architecture Decisions

### Why Terminal-Based?
- **Universal compatibility**: Works on any system with Python
- **Lightweight**: No GUI dependencies
- **Nostalgic**: Captures retro gaming feel
- **Accessible**: Works over SSH and remote connections

### Why JSON for Saves?
- **Human readable**: Easy to debug and modify
- **Built-in support**: No external dependencies
- **Flexible**: Easy to add new fields
- **Portable**: Works across platforms

### Why Single File?
- **Simplicity**: Easy to understand and modify
- **Portability**: Single file to share
- **Learning**: Good for studying game development
- **Future**: Can be refactored into modules later

---

## Future Roadmap

### Short Term (v1.x)
- [ ] Bug fixes and stability improvements
- [ ] Better ASCII art and animations
- [ ] Sound effects (beeps)
- [ ] Configuration file support

### Medium Term (v2.x)
- [ ] Multiple pets in single session
- [ ] Pet breeding and genetics
- [ ] Mini-games and activities
- [ ] Achievement system

### Long Term (v3.x)
- [ ] Graphical interface option
- [ ] Network multiplayer features
- [ ] Mobile app version
- [ ] AI-powered pet personalities

---

Happy coding! 🍄✨


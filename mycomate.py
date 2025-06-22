#!/usr/bin/env python3
"""
MycoMate - Your Digital Mushroom Pet
A Tamagotchi-style game where you care for a growing mushroom!
"""

import json
import time
import random
import os
import sys
from datetime import datetime, timedelta

# Color constants for terminal output
class Colors:
    GREEN = '\033[92m'  # Positive changes
    RED = '\033[91m'    # Negative changes  
    YELLOW = '\033[93m' # Warnings
    BLUE = '\033[94m'   # Info
    PURPLE = '\033[95m' # Special events
    CYAN = '\033[96m'   # Highlights
    BOLD = '\033[1m'    # Bold text
    RESET = '\033[0m'   # Reset to default

class MushroomPet:
    def __init__(self, name="Sporeling"):
        self.name = name
        self.birth_time = time.time()
        self.last_update = time.time()
        
        # Pet stats (0-100)
        self.hunger = 50
        self.happiness = 50
        self.health = 100
        self.cleanliness = 100
        self.energy = 80
        
        # Growth and evolution
        self.age = 0  # in hours
        self.growth_stage = 0  # 0=spore, 1=sprout, 2=young, 3=mature, 4=magical
        self.size = 1
        
        # Special attributes
        self.personality = random.choice(['shy', 'playful', 'curious', 'sleepy', 'energetic'])
        self.favorite_food = random.choice(['water', 'compost', 'sunshine', 'minerals'])
        self.mood = 'content'
        
        # Game mechanics
        self.last_fed = time.time()
        self.last_played = time.time()
        self.last_cleaned = time.time()
        self.experience = 0
        self.level = 1
        
        # File for persistence
        self.save_file = f".mushroom_pet_{name.lower()}.json"
        
    def get_age_in_hours(self):
        """Calculate age in hours"""
        return (time.time() - self.birth_time) / 3600
    
    def update_stats(self):
        """Update pet stats based on time passage"""
        current_time = time.time()
        time_passed = (current_time - self.last_update) / 3600  # in hours
        
        if time_passed < 0.01:  # Less than 36 seconds, no update needed
            return
            
        # Stats decay over time
        self.hunger = max(0, self.hunger - (time_passed * 5))
        self.happiness = max(0, self.happiness - (time_passed * 3))
        self.cleanliness = max(0, self.cleanliness - (time_passed * 2))
        self.energy = max(0, self.energy - (time_passed * 4))
        
        # Health is affected by other stats
        if self.hunger < 20 or self.cleanliness < 30:
            self.health = max(0, self.health - (time_passed * 8))
        elif self.hunger > 80 and self.cleanliness > 70 and self.happiness > 60:
            self.health = min(100, self.health + (time_passed * 2))
        
        # Age and growth
        self.age = self.get_age_in_hours()
        old_stage = self.growth_stage
        
        if self.age > 72 and self.health > 80 and self.experience > 500:  # 3 days + conditions
            self.growth_stage = 4  # magical
        elif self.age > 48 and self.health > 60:  # 2 days
            self.growth_stage = 3  # mature
        elif self.age > 24 and self.health > 40:  # 1 day
            self.growth_stage = 2  # young
        elif self.age > 6:  # 6 hours
            self.growth_stage = 1  # sprout
        
        if self.growth_stage > old_stage:
            self.experience += 100  # Bonus for growing
            # Store evolution info for later display
            self._evolution_celebration = self.get_growth_celebration(self.growth_stage)
            
        # Update mood based on stats
        self.update_mood()
        
        self.last_update = current_time
    
    def update_mood(self):
        """Update mood based on current stats"""
        avg_stats = (self.hunger + self.happiness + self.health + self.cleanliness + self.energy) / 5
        
        if avg_stats > 80:
            self.mood = random.choice(['ecstatic', 'joyful', 'blissful'])
        elif avg_stats > 60:
            self.mood = random.choice(['happy', 'content', 'cheerful'])
        elif avg_stats > 40:
            self.mood = random.choice(['okay', 'neutral', 'meh'])
        elif avg_stats > 20:
            self.mood = random.choice(['sad', 'worried', 'tired'])
        else:
            self.mood = random.choice(['miserable', 'sick', 'dying'])
    
    def get_ascii_art(self):
        """Get ASCII art based on growth stage and mood"""
        arts = {
            0: {  # spore
                'happy': "  ○\n  ·",
                'sad': "  ○\n  .",
                'default': "  ●\n  ·"
            },
            1: {  # sprout
                'happy': "  |\n ○○\n  |",
                'sad': "  |\n ●●\n  |",
                'default': "  |\n ◦◦\n  |"
            },
            2: {  # young
                'happy': "  🍄\n ◉ ◉\n  \\_/",
                'sad': "  🍄\n ● ●\n  ___",
                'default': "  🍄\n ○ ○\n  ~~"
            },
            3: {  # mature
                'happy': "   🍄🍄\n  ^◉ ◉^\n   \\_/\n    |",
                'sad': "   🍄🍄\n  ×● ●×\n   ___\n    |",
                'default': "   🍄🍄\n  ○ ○ ○\n   ~~~\n    |"
            },
            4: {  # magical
                'happy': " ✨🍄✨🍄✨\n  ^◉   ◉^\n   \\___/\n  ~~~ ~~~",
                'sad': " ⚡🍄⚡🍄⚡\n  ×●   ●×\n   _____\n  --- ---",
                'default': " ★ 🍄★🍄 ★\n  ◐   ◑\n   ~~~~~\n  ≋≋≋≋≋"
            }
        }
        
        stage_art = arts.get(self.growth_stage, arts[0])
        
        if self.mood in ['happy', 'ecstatic', 'joyful', 'blissful', 'cheerful']:
            return stage_art.get('happy', stage_art['default'])
        elif self.mood in ['sad', 'miserable', 'sick', 'dying', 'worried']:
            return stage_art.get('sad', stage_art['default'])
        else:
            return stage_art['default']
    
    def get_stage_name(self):
        """Get the name of current growth stage"""
        stages = ['Spore', 'Sprout', 'Young Mushroom', 'Mature Mushroom', 'Magical Mushroom']
        return stages[self.growth_stage]
    
    def format_stat_change(self, stat_name, old_value, new_value):
        """Format stat changes with colors and visual indicators"""
        change = new_value - old_value
        if change > 0:
            return f"{Colors.GREEN}+{change:.0f} {stat_name}{Colors.RESET}"
        elif change < 0:
            return f"{Colors.RED}{change:.0f} {stat_name}{Colors.RESET}"
        else:
            return f"0 {stat_name}"
    
    def get_level_up_celebration(self, new_level):
        """Create celebration message for level ups"""
        celebration = f"""
{Colors.YELLOW}╔════════════════════════════════════════╗{Colors.RESET}
{Colors.YELLOW}║{Colors.RESET}  🎉 {Colors.BOLD}LEVEL UP!{Colors.RESET} 🎉                  {Colors.YELLOW}║{Colors.RESET}
{Colors.YELLOW}║{Colors.RESET}                                      {Colors.YELLOW}║{Colors.RESET}
{Colors.YELLOW}║{Colors.RESET}    {self.name} reached Level {new_level}!{' ' * (16 - len(str(new_level)) - len(self.name))} {Colors.YELLOW}║{Colors.RESET}
{Colors.YELLOW}║{Colors.RESET}                                      {Colors.YELLOW}║{Colors.RESET}
{Colors.YELLOW}║{Colors.RESET}     ✨ New abilities unlocked! ✨     {Colors.YELLOW}║{Colors.RESET}
{Colors.YELLOW}╚════════════════════════════════════════╝{Colors.RESET}
"""
        return celebration
    
    def get_growth_celebration(self, new_stage):
        """Create celebration message for growth stage evolution"""
        stage_names = ['Spore', 'Sprout', 'Young Mushroom', 'Mature Mushroom', 'Magical Mushroom']
        stage_emojis = ['🌱', '🌿', '🍄', '🍄🍄', '✨🍄✨']
        
        celebration = f"""
{Colors.PURPLE}╔════════════════════════════════════════╗{Colors.RESET}
{Colors.PURPLE}║{Colors.RESET}  🌟 {Colors.BOLD}EVOLUTION!{Colors.RESET} 🌟                  {Colors.PURPLE}║{Colors.RESET}
{Colors.PURPLE}║{Colors.RESET}                                      {Colors.PURPLE}║{Colors.RESET}
{Colors.PURPLE}║{Colors.RESET}  {self.name} evolved into a {stage_names[new_stage]}!{' ' * (8 - len(stage_names[new_stage]) - len(self.name))} {Colors.PURPLE}║{Colors.RESET}
{Colors.PURPLE}║{Colors.RESET}                                      {Colors.PURPLE}║{Colors.RESET}
{Colors.PURPLE}║{Colors.RESET}          {stage_emojis[new_stage-1]} → {stage_emojis[new_stage]}          {Colors.PURPLE}║{Colors.RESET}
{Colors.PURPLE}╚════════════════════════════════════════╝{Colors.RESET}
"""
        return celebration

    def feed(self, food_type='nutrients'):
        """Feed the pet"""
        current_time = time.time()
        
        # Check if actually hungry first
        if self.hunger > 85:
            return f"🥱 {self.name} is not hungry right now! {Colors.YELLOW}(Hunger: {self.hunger:.0f}%){Colors.RESET}"
        
        # Only apply cooldown if recently fed AND not very hungry
        time_since_fed = current_time - self.last_fed
        if time_since_fed < 1800 and self.hunger > 60:  # 30 min cooldown, but only if not very hungry
            minutes_left = (1800 - time_since_fed) / 60
            return f"⏰ {self.name} is still digesting! Try again in {Colors.YELLOW}{minutes_left:.0f} minutes{Colors.RESET}."
        
        food_effects = {
            'nutrients': (25, 5, 5),
            'compost': (20, 10, 0),
            'water': (15, 5, 10),
            'sunshine': (10, 15, 15),
            'minerals': (30, 0, 8)
        }
        
        hunger_gain, happiness_gain, health_gain = food_effects.get(food_type, (20, 5, 5))
        
        # Store old values for comparison
        old_hunger = self.hunger
        old_happiness = self.happiness
        old_health = self.health
        old_experience = self.experience
        old_level = self.level
        
        # Bonus if it's their favorite food
        is_favorite = food_type == self.favorite_food
        if is_favorite:
            hunger_gain += 10
            happiness_gain += 15
            self.experience += 20
        
        # Apply changes
        self.hunger = min(100, self.hunger + hunger_gain)
        self.happiness = min(100, self.happiness + happiness_gain)
        self.health = min(100, self.health + health_gain)
        self.last_fed = current_time
        self.experience += 10
        
        # Check for level up
        new_level = 1 + (self.experience // 100)
        leveled_up = new_level > old_level
        if leveled_up:
            self.level = new_level
        
        # Create stat change display
        changes = []
        if self.hunger > old_hunger:
            changes.append(self.format_stat_change("🍽️ Hunger", old_hunger, self.hunger))
        if self.happiness > old_happiness:
            changes.append(self.format_stat_change("😊 Happiness", old_happiness, self.happiness))
        if self.health > old_health:
            changes.append(self.format_stat_change("❤️ Health", old_health, self.health))
        if self.experience > old_experience:
            changes.append(self.format_stat_change("⭐ XP", old_experience, self.experience))
        
        change_text = " | ".join(changes) if changes else ""
        
        # Enhanced responses with personality
        personality_responses = {
            'shy': [
                f"🤗 {self.name} quietly nibbles the {food_type}...",
                f"😊 {self.name} seems pleased with the {food_type}.",
                f"🙂 *soft munching* {self.name} enjoys their meal."
            ],
            'playful': [
                f"🎉 {self.name} bounces excitedly while eating {food_type}!",
                f"😄 *happy wiggling* {self.name} loves this {food_type}!",
                f"🤸 {self.name} does a little dance before eating!"
            ],
            'curious': [
                f"🔍 {self.name} carefully examines the {food_type} before eating.",
                f"🤔 {self.name} seems intrigued by this {food_type}!",
                f"👁️ {self.name} studies the {food_type} with interest."
            ],
            'sleepy': [
                f"😴 {self.name} drowsily munches on the {food_type}...",
                f"🥱 *yawn* {self.name} slowly enjoys their {food_type}.",
                f"💤 {self.name} eating makes them even more relaxed."
            ],
            'energetic': [
                f"⚡ {self.name} quickly devours the {food_type}!",
                f"🚀 {self.name} enthusiastically chomps the {food_type}!",
                f"💨 *rapid munching* {self.name} can't wait to eat!"
            ]
        }
        
        base_response = random.choice(personality_responses.get(self.personality, [
            f"🍄 {self.name} happily munches on the {food_type}! *nom nom*",
            f"😋 {self.name} seems to really enjoy the {food_type}!",
            f"🤤 *munch munch* {self.name} is satisfied!"
        ]))
        
        # Add favorite food bonus message
        if is_favorite:
            base_response += f" ✨ {Colors.CYAN}It's their favorite!{Colors.RESET} ✨"
        
        # Combine response with stat changes
        full_response = f"{base_response}\n{change_text}"
        
        # Add level up celebration if applicable
        if leveled_up:
            full_response += "\n\n" + self.get_level_up_celebration(new_level)
        
        return full_response
    
    def play(self):
        """Play with the pet"""
        current_time = time.time()
        
        if current_time - self.last_played < 1200:  # 20 minutes cooldown
            minutes_left = (1200 - (current_time - self.last_played)) / 60
            return f"😴 {self.name} needs to rest between play sessions! Try again in {Colors.YELLOW}{minutes_left:.0f} minutes{Colors.RESET}."
        
        if self.energy < 30:  # Increased threshold to avoid the gap
            return f"😫 {self.name} is too tired to play! {Colors.RED}(Energy: {self.energy:.0f}%){Colors.RESET} Let them rest first."
        
        # Personality-based play activities
        personality_activities = {
            'shy': [
                "quietly exploring hidden spots",
                "gentle leaf rustling",
                "peaceful meditation",
                "soft spore floating"
            ],
            'playful': [
                "bouncy mushroom dancing",
                "energetic cap wiggling",
                "playful rolling around",
                "joyful spore celebrations"
            ],
            'curious': [
                "investigating interesting smells",
                "examining tiny creatures",
                "studying soil patterns",
                "exploring new territories"
            ],
            'sleepy': [
                "dreamy swaying motions",
                "relaxed stretching",
                "gentle breathing exercises",
                "cozy burrowing games"
            ],
            'energetic': [
                "high-speed spore racing",
                "rapid growth competitions",
                "intense soil digging",
                "lightning-fast dancing"
            ]
        }
        
        activities = personality_activities.get(self.personality, [
            "hide and seek among the leaves",
            "rolling in the dirt",
            "dancing in the moonlight",
            "practicing spore dispersal"
        ])
        
        activity = random.choice(activities)
        
        # Store old values for comparison
        old_happiness = self.happiness
        old_energy = self.energy
        old_experience = self.experience
        old_level = self.level
        
        # Apply changes
        self.happiness = min(100, self.happiness + 20)
        self.energy = max(0, self.energy - 15)
        self.experience += 15
        self.last_played = current_time
        
        # Check for level up
        new_level = 1 + (self.experience // 100)
        leveled_up = new_level > old_level
        if leveled_up:
            self.level = new_level
        
        # Create stat change display
        changes = []
        if self.happiness > old_happiness:
            changes.append(self.format_stat_change("😊 Happiness", old_happiness, self.happiness))
        if self.energy < old_energy:
            changes.append(self.format_stat_change("⚡ Energy", old_energy, self.energy))
        if self.experience > old_experience:
            changes.append(self.format_stat_change("⭐ XP", old_experience, self.experience))
        
        change_text = " | ".join(changes) if changes else ""
        
        # Personality-based responses
        personality_responses = {
            'shy': [
                f"🤗 {self.name} shyly enjoys {activity}...",
                f"😌 {self.name} seems content after {activity}.",
                f"🙂 *quiet happiness* {self.name} had fun!"
            ],
            'playful': [
                f"🎉 {self.name} has a blast {activity}!",
                f"😄 *joyful bouncing* {self.name} loves {activity}!",
                f"🤸 {self.name} can't stop giggling after {activity}!"
            ],
            'curious': [
                f"🔍 {self.name} discovers something interesting while {activity}!",
                f"🤔 {self.name} learns something new from {activity}!",
                f"💡 {activity} sparks {self.name}'s curiosity!"
            ],
            'sleepy': [
                f"😴 {self.name} drowsily enjoys {activity}...",
                f"🥱 {activity} was relaxing for {self.name}.",
                f"💤 {self.name} feels peacefully tired after {activity}."
            ],
            'energetic': [
                f"⚡ {self.name} energetically tackles {activity}!",
                f"🚀 {self.name} puts maximum effort into {activity}!",
                f"💨 {self.name} zooms through {activity} with enthusiasm!"
            ]
        }
        
        base_response = random.choice(personality_responses.get(self.personality, [
            f"🎮 {self.name} enjoys {activity}! Their cap wiggles with joy!",
            f"😊 You and {self.name} have fun {activity}!",
            f"🎈 {self.name} seems much happier after {activity}!"
        ]))
        
        # Combine response with stat changes
        full_response = f"{base_response}\n{change_text}"
        
        # Add level up celebration if applicable
        if leveled_up:
            full_response += "\n\n" + self.get_level_up_celebration(new_level)
        
        return full_response
    
    def clean(self):
        """Clean the pet"""
        current_time = time.time()
        
        if current_time - self.last_cleaned < 3600:  # 1 hour cooldown
            time_left = (3600 - (current_time - self.last_cleaned)) / 60
            return f"✨ {self.name} is already clean! {Colors.YELLOW}(Next cleaning in {time_left:.0f} minutes){Colors.RESET}"
        
        # Check cleanliness level
        if self.cleanliness > 90:
            return f"🧼 {self.name} is already sparkling clean! {Colors.YELLOW}(Cleanliness: {self.cleanliness:.0f}%){Colors.RESET}"
        
        # Store old values for comparison
        old_cleanliness = self.cleanliness
        old_happiness = self.happiness
        old_health = self.health
        old_experience = self.experience
        old_level = self.level
        
        # Apply changes
        self.cleanliness = 100
        self.happiness = min(100, self.happiness + 10)
        self.health = min(100, self.health + 5)
        self.last_cleaned = current_time
        self.experience += 8
        
        # Check for level up
        new_level = 1 + (self.experience // 100)
        leveled_up = new_level > old_level
        if leveled_up:
            self.level = new_level
        
        # Create stat change display
        changes = []
        if self.cleanliness > old_cleanliness:
            changes.append(self.format_stat_change("🧼 Cleanliness", old_cleanliness, self.cleanliness))
        if self.happiness > old_happiness:
            changes.append(self.format_stat_change("😊 Happiness", old_happiness, self.happiness))
        if self.health > old_health:
            changes.append(self.format_stat_change("❤️ Health", old_health, self.health))
        if self.experience > old_experience:
            changes.append(self.format_stat_change("⭐ XP", old_experience, self.experience))
        
        change_text = " | ".join(changes) if changes else ""
        
        # Personality-based responses
        personality_responses = {
            'shy': [
                f"🤗 {self.name} quietly enjoys the gentle cleaning...",
                f"😌 {self.name} seems relaxed during their spa time.",
                f"🙂 *soft contentment* {self.name} feels much better now."
            ],
            'playful': [
                f"🎉 {self.name} splashes happily during bath time!",
                f"😄 {self.name} makes bubbles and giggles!",
                f"🤸 {self.name} does happy wiggles while being cleaned!"
            ],
            'curious': [
                f"🔍 {self.name} examines each bubble with interest!",
                f"🤔 {self.name} seems fascinated by the cleaning process!",
                f"👁️ {self.name} watches the dirt wash away curiously."
            ],
            'sleepy': [
                f"😴 {self.name} drowsily enjoys the warm, soothing bath...",
                f"🥱 *yawn* The cleaning is very relaxing for {self.name}.",
                f"💤 {self.name} almost falls asleep during the spa treatment."
            ],
            'energetic': [
                f"⚡ {self.name} enthusiastically helps with the cleaning!",
                f"🚀 {self.name} can't sit still during bath time!",
                f"💨 {self.name} is excited to get squeaky clean!"
            ]
        }
        
        base_response = random.choice(personality_responses.get(self.personality, [
            f"✨ {self.name} sparkles after a good cleaning!",
            f"🧼 You gently brush off {self.name}'s cap. They look refreshed!",
            f"🛁 {self.name} enjoys the spa treatment!",
            f"🌟 All the dirt and debris are gone. {self.name} looks pristine!"
        ]))
        
        # Combine response with stat changes
        full_response = f"{base_response}\n{change_text}"
        
        # Add level up celebration if applicable
        if leveled_up:
            full_response += "\n\n" + self.get_level_up_celebration(new_level)
        
        return full_response
    
    def rest(self):
        """Let the pet rest"""
        if self.energy > 90:
            return f"⚡ {self.name} is already well-rested! {Colors.YELLOW}(Energy: {self.energy:.0f}%){Colors.RESET}"
        
        # Store old values for comparison
        old_energy = self.energy
        old_health = self.health
        old_experience = self.experience
        old_level = self.level
        
        # Apply changes
        energy_gain = min(30, 100 - self.energy)  # Don't go over 100
        self.energy = min(100, self.energy + energy_gain)
        self.health = min(100, self.health + 5)
        self.experience += 5
        
        # Check for level up
        new_level = 1 + (self.experience // 100)
        leveled_up = new_level > old_level
        if leveled_up:
            self.level = new_level
        
        # Create stat change display
        changes = []
        if self.energy > old_energy:
            changes.append(self.format_stat_change("⚡ Energy", old_energy, self.energy))
        if self.health > old_health:
            changes.append(self.format_stat_change("❤️ Health", old_health, self.health))
        if self.experience > old_experience:
            changes.append(self.format_stat_change("⭐ XP", old_experience, self.experience))
        
        change_text = " | ".join(changes) if changes else ""
        
        # Personality-based responses
        personality_responses = {
            'shy': [
                f"🤗 {self.name} quietly curls up for a peaceful rest...",
                f"😌 {self.name} finds a cozy, hidden spot to nap.",
                f"🙂 *soft snoring* {self.name} dreams sweetly."
            ],
            'playful': [
                f"🎉 {self.name} bounces into their favorite sleeping spot!",
                f"😄 {self.name} does a happy spin before settling down!",
                f"🤸 Even while resting, {self.name} wiggles with joy!"
            ],
            'curious': [
                f"🔍 {self.name} examines their sleeping area before resting.",
                f"🤔 {self.name} wonders what dreams will come!",
                f"👁️ {self.name} studies the patterns in the soil while dozing."
            ],
            'sleepy': [
                f"😴 {self.name} yawns and easily drifts off to sleep...",
                f"🥱 *stretch* {self.name} was ready for this nap!",
                f"💤 {self.name} falls into the deepest, most restful sleep."
            ],
            'energetic': [
                f"⚡ {self.name} reluctantly slows down for a power nap!",
                f"🚀 {self.name} charges up their energy reserves!",
                f"💨 Even while resting, {self.name} seems ready to go!"
            ]
        }
        
        base_response = random.choice(personality_responses.get(self.personality, [
            f"💤 {self.name} takes a peaceful nap and feels refreshed!",
            f"🛏️ {self.name} burrows into the soil for a cozy rest.",
            f"😴 Zzz... {self.name} has sweet mushroom dreams!",
            f"🌙 {self.name} absorbs energy from the earth while resting."
        ]))
        
        # Combine response with stat changes
        full_response = f"{base_response}\n{change_text}"
        
        # Add level up celebration if applicable
        if leveled_up:
            full_response += "\n\n" + self.get_level_up_celebration(new_level)
        
        return full_response
    
    def get_status(self):
        """Get detailed status of the pet"""
        self.update_stats()
        
        # Status bars
        def make_bar(value, length=10):
            filled = int((value / 100) * length)
            bar = "█" * filled + "░" * (length - filled)
            return f"[{bar}] {value:.0f}%"
        
        status = f"""
╔══════════════════════════════════════╗
║           🍄 {self.name} 🍄            ║
╠══════════════════════════════════════╣
║                                      ║
{self.get_ascii_art()}
║                                      ║
╠══════════════════════════════════════╣
║ Stage: {self.get_stage_name():<26} ║
║ Age: {self.age:.1f} hours{' ' * (28 - len(f'{self.age:.1f} hours'))}║
║ Mood: {self.mood.title():<27} ║
║ Personality: {self.personality.title():<22} ║
║                                      ║
║ Hunger:      {make_bar(self.hunger):<15} ║
║ Happiness:   {make_bar(self.happiness):<15} ║
║ Health:      {make_bar(self.health):<15} ║
║ Cleanliness: {make_bar(self.cleanliness):<15} ║
║ Energy:      {make_bar(self.energy):<15} ║
║                                      ║
║ Level: {self.level:<5} Experience: {self.experience:<8} ║
║ Favorite Food: {self.favorite_food.title():<18} ║
╚══════════════════════════════════════╝
"""
        return status
    
    def save_to_file(self):
        """Save pet data to file"""
        data = {
            'name': self.name,
            'birth_time': self.birth_time,
            'last_update': time.time(),
            'hunger': self.hunger,
            'happiness': self.happiness,
            'health': self.health,
            'cleanliness': self.cleanliness,
            'energy': self.energy,
            'age': self.age,
            'growth_stage': self.growth_stage,
            'personality': self.personality,
            'favorite_food': self.favorite_food,
            'mood': self.mood,
            'last_fed': self.last_fed,
            'last_played': self.last_played,
            'last_cleaned': self.last_cleaned,
            'experience': self.experience,
            'level': self.level
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def load_from_file(self):
        """Load pet data from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                
                # Update stats based on time away
                self.update_stats()
                return True
        except Exception as e:
            print(f"Error loading: {e}")
        return False

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear')

def draw_ui(pet):
    """Draw the complete UI with pet status always visible"""
    clear_screen()
    
    # Update pet stats
    pet.update_stats()
    
    # Get terminal dimensions for responsive design
    width = os.get_terminal_size().columns
    width = min(80, width)  # Cap at 80 for readability
    
    # Create status bars
    def make_bar(value, length=12, filled_char="█", empty_char="░"):
        filled = int((value / 100) * length)
        bar = filled_char * filled + empty_char * (length - filled)
        return f"[{bar}] {value:.0f}%"
    
    # Get color based on stat value
    def get_stat_color(value):
        if value > 70:
            return "\033[32m"  # Green
        elif value > 40:
            return "\033[33m"  # Yellow
        else:
            return "\033[31m"  # Red
    
    reset_color = "\033[0m"
    
    # Main display
    print("╔" + "═" * (width - 2) + "╗")
    
    # Title line
    title = f"🍄 MycoMate - {pet.name} 🍄"
    title_padding = (width - len(title) - 2) // 2
    print(f"║{' ' * title_padding}{title}{' ' * (width - len(title) - title_padding - 2)}║")
    
    print("╠" + "═" * (width - 2) + "╣")
    
    # Pet display area
    pet_art = pet.get_ascii_art()
    art_lines = pet_art.split('\n')
    
    # Pet info
    info_lines = [
        f"Stage: {pet.get_stage_name()}",
        f"Age: {pet.age:.1f} hours",
        f"Mood: {pet.mood.title()}",
        f"Personality: {pet.personality.title()}"
    ]
    
    # Display pet and info
    max_lines = max(len(art_lines), len(info_lines))
    
    for i in range(max_lines):
        art_part = art_lines[i] if i < len(art_lines) else ""
        info_part = info_lines[i] if i < len(info_lines) else ""
        
        # Simple layout: art on left, info on right
        line = f"║  {art_part:<20} {info_part}"
        padding = width - len(line) - 1
        print(f"{line}{' ' * max(0, padding)}║")
    
    print("╠" + "═" * (width - 2) + "╣")
    
    # Stats display
    stats = [
        ("🍽️", "Hunger", pet.hunger),
        ("😊", "Happiness", pet.happiness),
        ("❤️", "Health", pet.health),
        ("🧼", "Cleanliness", pet.cleanliness),
        ("⚡", "Energy", pet.energy)
    ]
    
    for emoji, name, value in stats:
        color = get_stat_color(value)
        bar = make_bar(value)
        line = f"║ {emoji} {name}: {color}{bar}{reset_color}"
        padding = width - len(line) + len(color) + len(reset_color) - 1
        print(f"{line}{' ' * max(0, padding)}║")
    
    print("╠" + "═" * (width - 2) + "╣")
    
    # Experience and level
    exp_bar = make_bar((pet.experience % 100), 12, "▓", "▒")
    line = f"║ 🌟 Level {pet.level} - XP: {exp_bar} ({pet.experience} total)"
    padding = width - len(line) - 1
    print(f"{line}{' ' * max(0, padding)}║")
    
    # Favorite food
    line = f"║ 💖 Favorite Food: {pet.favorite_food.title()}"
    padding = width - len(line) - 1
    print(f"{line}{' ' * max(0, padding)}║")
    
    print("╚" + "═" * (width - 2) + "╝")
    print()

def show_menu():
    """Display the action menu"""
    print("What would you like to do?")
    print("1. 🍽️  Feed Pet     2. 🎮 Play        3. 🧼 Clean")
    print("4. 😴 Rest         5. 💾 Save & Quit  6. ❓ Help")
    
def show_help():
    """Show help information"""
    help_text = """
🍄 MycoMate Help 🍄

Your mushroom pet needs regular care to grow and thrive!

STATS EXPLAINED:
• Hunger: Feed your pet regularly with different foods
• Happiness: Play with your pet to keep them joyful
• Health: Maintain good overall care for high health
• Cleanliness: Clean your pet when they get dirty
• Energy: Let your pet rest when they're tired

GROWTH STAGES:
Spore → Sprout → Young → Mature → Magical Mushroom

TIPS:
• Each pet has a favorite food that gives bonus benefits
• Different personalities affect how your pet behaves
• Experience points help your pet grow and evolve
• Save regularly to keep your progress!

FOOD TYPES:
• nutrients: Good all-around food
• compost: Great for hunger, some happiness
• water: Moderate hunger, good for energy
• sunshine: Moderate hunger, great happiness and energy  
• minerals: Excellent for hunger, good for health
"""
    print(help_text)

def main():
    """Main game loop"""
    print("🍄 Starting MycoMate...")
    
    # Check if save file exists
    save_files = [f for f in os.listdir('.') if f.startswith('.mushroom_pet_') and f.endswith('.json')]
    
    if save_files:
        print(f"\nFound existing pets: {', '.join([f.split('_')[2].split('.')[0].title() for f in save_files])}")
        pet_name = input("Enter pet name to load (or new name to create): ").strip()
    else:
        pet_name = input("Enter a name for your new mushroom pet: ").strip()
    
    if not pet_name:
        pet_name = "Sporeling"
    
    pet = MushroomPet(pet_name)
    
    # Try to load existing pet
    if not pet.load_from_file():
        print(f"\n🌱 A new {pet.personality} spore named {pet.name} has sprouted!")
        print(f"Their favorite food is {pet.favorite_food}!")
    else:
        print(f"\n🍄 Welcome back, {pet.name}!")
        time_away = (time.time() - pet.last_update) / 3600
        if time_away > 1:
            print(f"You were away for {time_away:.1f} hours. Let's see how {pet.name} is doing...")
    
    input("\nPress Enter to continue...")
    
    while True:
        # Draw the full UI with pet status
        draw_ui(pet)
        
        # Show menu
        show_menu()
        choice = input("\n> ").strip()
        
        result_message = ""
        
        if choice == '1':
            print("\nFood options: nutrients, compost, water, sunshine, minerals")
            food = input("What would you like to feed them? ").strip().lower()
            if food in ['nutrients', 'compost', 'water', 'sunshine', 'minerals']:
                result_message = pet.feed(food)
            else:
                result_message = pet.feed()  # Default food
        elif choice == '2':
            result_message = pet.play()
        elif choice == '3':
            result_message = pet.clean()
        elif choice == '4':
            result_message = pet.rest()
        elif choice == '5':
            if pet.save_to_file():
                print(f"\n💾 {pet.name} has been saved! See you later! 🍄")
            else:
                print("\n❌ Error saving. Try again!")
            break
        elif choice == '6':
            clear_screen()
            show_help()
            input("\nPress Enter to continue...")
            continue
        else:
            result_message = "❌ Invalid choice! Please try again."
        
        # Show result message if there is one
        if result_message:
            print(f"\n🍄 {result_message}")
            input("\nPress Enter to continue...")
        
        # Check for evolution celebration (triggered by update_stats)
        if hasattr(pet, '_evolution_celebration'):
            print("\n" + pet._evolution_celebration)
            delattr(pet, '_evolution_celebration')  # Remove after showing
            input("\nPress Enter to continue...")
        
        # Auto-save periodically
        if random.randint(1, 5) == 1:
            pet.save_to_file()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🍄 Thanks for playing MycoMate! 🍄")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Your pet data should still be safe!")


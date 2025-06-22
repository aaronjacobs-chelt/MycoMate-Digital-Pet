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
            
        # Improved stat decay rates for better balance
        # Base decay rates per hour (reduced for better playability)
        hunger_decay = 4  # Was 5, reduced to be less aggressive
        happiness_decay = 2.5  # Was 3, slightly reduced
        cleanliness_decay = 1.5  # Was 2, reduced as cleaning has 1hr cooldown
        energy_decay = 3.5  # Was 4, slightly reduced
        
        # Personality affects decay rates - each with distinct characteristics
        if self.personality == 'energetic':
            energy_decay *= 1.3  # Burns energy much faster from constant activity
            hunger_decay *= 1.2  # High metabolism from being active
            cleanliness_decay *= 1.1  # Gets dirty from being active
        elif self.personality == 'sleepy':
            energy_decay *= 0.6  # Conserves energy very well
            happiness_decay *= 1.2  # Gets sad easier without stimulation
            hunger_decay *= 0.9  # Slower metabolism when resting
        elif self.personality == 'playful':
            happiness_decay *= 0.7  # Maintains happiness much better
            energy_decay *= 1.1  # Uses energy for play but not excessively
        elif self.personality == 'shy':
            cleanliness_decay *= 0.7  # Stays much cleaner (hides and avoids mess)
            happiness_decay *= 1.3  # Needs significantly more attention
            energy_decay *= 0.9  # Conserves energy by hiding
        elif self.personality == 'curious':
            energy_decay *= 1.15  # Uses energy exploring
            hunger_decay *= 1.05  # Burns some calories investigating
            happiness_decay *= 0.85  # Exploration keeps them fairly content
        
        # Apply decay
        self.hunger = max(0, self.hunger - (time_passed * hunger_decay))
        self.happiness = max(0, self.happiness - (time_passed * happiness_decay))
        self.cleanliness = max(0, self.cleanliness - (time_passed * cleanliness_decay))
        self.energy = max(0, self.energy - (time_passed * energy_decay))
        
        # Improved health system with more granular changes
        health_change = 0
        
        # Negative health factors
        if self.hunger < 20:
            health_change -= time_passed * 6  # Was 8, reduced severity
        if self.cleanliness < 30:
            health_change -= time_passed * 4
        if self.happiness < 15:
            health_change -= time_passed * 2  # Very sad pets get sick
        if self.energy < 10:
            health_change -= time_passed * 1  # Exhaustion affects health
        
        # Positive health factors (more achievable conditions)
        good_care_stats = 0
        if self.hunger > 60: good_care_stats += 1
        if self.cleanliness > 60: good_care_stats += 1
        if self.happiness > 50: good_care_stats += 1
        if self.energy > 40: good_care_stats += 1
        
        if good_care_stats >= 3:
            health_change += time_passed * 2
        elif good_care_stats >= 2:
            health_change += time_passed * 0.5
        
        # Apply health change
        self.health = max(0, min(100, self.health + health_change))
        
        # Age and growth
        self.age = self.get_age_in_hours()
        old_stage = self.growth_stage
        
        # Improved growth requirements for better progression balance
        if self.age > 48 and self.health > 75 and self.experience >= 400:  # 2 days + conditions (reduced from 72hrs and 500xp)
            self.growth_stage = 4  # magical
        elif self.age > 30 and self.health > 50:  # 30 hours (reduced from 48)
            self.growth_stage = 3  # mature
        elif self.age > 16 and self.health > 35:  # 16 hours (reduced from 24)
            self.growth_stage = 2  # young
        elif self.age > 4:  # 4 hours (reduced from 6)
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
        
        # Rebalanced food effects (hunger, happiness, health)
        food_effects = {
            'nutrients': (20, 8, 5),      # Balanced nutrition (reduced hunger gain, increased happiness)
            'compost': (25, 5, 3),        # High hunger, low happiness, some health
            'water': (12, 3, 2),          # Light meal, hydration focused
            'sunshine': (8, 18, 8),       # Low hunger, high happiness and health
            'minerals': (28, 2, 12)       # Very high hunger, low happiness, good health
        }
        
        hunger_gain, happiness_gain, health_gain = food_effects.get(food_type, (20, 5, 5))
        
        # Store old values for comparison
        old_hunger = self.hunger
        old_happiness = self.happiness
        old_health = self.health
        old_experience = self.experience
        old_level = self.level
        
        # Enhanced favorite food bonus
        is_favorite = food_type == self.favorite_food
        if is_favorite:
            hunger_gain += 8   # Reduced from 10
            happiness_gain += 12  # Reduced from 15
            health_gain += 3   # Added health bonus for favorite food
            self.experience += 15  # Reduced from 20
        
        # Apply changes
        self.hunger = min(100, self.hunger + hunger_gain)
        self.happiness = min(100, self.happiness + happiness_gain)
        self.health = min(100, self.health + health_gain)
        self.last_fed = current_time
        
        # Improved XP distribution based on action quality
        base_xp = 8  # Reduced from 10
        if is_favorite:
            base_xp += 7  # Total 15 for favorite food
        if self.hunger < 30:  # Bonus for feeding when very hungry
            base_xp += 3
        
        self.experience += base_xp
        
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
        
        # Improved play effects with personality consideration
        happiness_gain = 18  # Reduced from 20
        energy_cost = 12     # Reduced from 15
        base_xp = 12         # Reduced from 15
        
        # Personality affects play effectiveness
        if self.personality == 'playful':
            happiness_gain += 5
            energy_cost -= 2
            base_xp += 3
        elif self.personality == 'energetic':
            energy_cost += 3
            base_xp += 2
        elif self.personality == 'sleepy':
            happiness_gain -= 3
            energy_cost += 2
        elif self.personality == 'shy':
            happiness_gain -= 2
            base_xp += 1  # Gets more satisfaction from overcoming shyness
        
        # Apply changes
        self.happiness = min(100, self.happiness + happiness_gain)
        self.energy = max(0, self.energy - energy_cost)
        
        # XP bonus for playing when pet is very happy or very sad
        if self.happiness > 80:
            base_xp += 2  # Reward maintaining high happiness
        elif self.happiness < 30:
            base_xp += 4  # Bigger reward for cheering up sad pet
        
        self.experience += base_xp
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
        
        # Improved cleaning effects
        cleanliness_before = self.cleanliness
        self.cleanliness = 100
        
        # Happiness and health gains based on how dirty they were
        dirtiness = 100 - cleanliness_before
        happiness_gain = 5 + (dirtiness * 0.1)  # More happiness if they were very dirty
        health_gain = 3 + (dirtiness * 0.08)    # More health benefit if they were very dirty
        
        self.happiness = min(100, self.happiness + happiness_gain)
        self.health = min(100, self.health + health_gain)
        self.last_cleaned = current_time
        
        # XP based on cleaning necessity
        base_xp = 6
        if cleanliness_before < 40:
            base_xp += 4  # Bonus for cleaning when very dirty
        elif cleanliness_before < 70:
            base_xp += 2  # Small bonus for regular maintenance
        
        self.experience += base_xp
        
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
        
        # Improved rest effects with personality consideration
        energy_before = self.energy
        energy_gain = min(25, 100 - self.energy)  # Reduced from 30
        
        # Personality affects rest effectiveness
        if self.personality == 'sleepy':
            energy_gain = min(35, 100 - self.energy)  # Sleepy pets rest better
        elif self.personality == 'energetic':
            energy_gain = min(20, 100 - self.energy)  # Energetic pets rest less efficiently
        
        self.energy = min(100, self.energy + energy_gain)
        
        # Health gain based on how tired they were
        tiredness = 100 - energy_before
        health_gain = 2 + (tiredness * 0.05)  # More health if they were very tired
        self.health = min(100, self.health + health_gain)
        
        # XP for rest (reduced and based on necessity)
        base_xp = 3  # Reduced from 5
        if energy_before < 30:
            base_xp += 3  # Bonus for resting when very tired
        
        self.experience += base_xp
        
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


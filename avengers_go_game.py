import random
import time
import math

class Avenger:
    def __init__(self, name, rarity, power_level, location_type):
        self.name = name
        self.rarity = rarity
        self.power_level = power_level
        self.location_type = location_type
        self.caught = False
    
    def __str__(self):
        return f"{self.name} (Power: {self.power_level}, Rarity: {self.rarity})"

class Location:
    def __init__(self, name, lat, lon, location_type):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.location_type = location_type
    
    def __str__(self):
        return f"{self.name} ({self.location_type})"

class Player:
    def __init__(self, name):
        self.name = name
        self.lat = 40.7128
        self.lon = -74.0060
        self.collection = []
        self.energy = 100
        self.level = 1
        self.experience = 0
    
    def move(self, direction, distance):
        """Move player in a direction"""
        if self.energy < 10:
            print("⚠️  Not enough energy! Rest to restore energy.")
            return False
        
        self.energy -= 10
        if direction == 'n':
            self.lat += distance * 0.01
        elif direction == 's':
            self.lat -= distance * 0.01
        elif direction == 'e':
            self.lon += distance * 0.01
        elif direction == 'w':
            self.lon -= distance * 0.01
        
        print(f"🚶 Moved {direction.upper()} - Energy: {self.energy}/100")
        return True
    
    def rest(self):
        """Restore energy"""
        self.energy = min(100, self.energy + 30)
        print(f"😌 Rested! Energy restored to {self.energy}/100")
    
    def add_avenger(self, avenger):
        """Add caught avenger to collection"""
        self.collection.append(avenger)
        xp_gain = avenger.power_level * (1 if avenger.rarity == "Common" else 2 if avenger.rarity == "Rare" else 3)
        self.experience += xp_gain
        print(f"✨ Gained {xp_gain} XP! Total XP: {self.experience}")
        
        # Level up
        if self.experience >= self.level * 100:
            self.level += 1
            print(f"🎉 LEVEL UP! You are now level {self.level}!")
    
    def distance_to(self, location):
        """Calculate distance to a location"""
        return math.sqrt((self.lat - location.lat)**2 + (self.lon - location.lon)**2)

class AvengersGO:
    def __init__(self):
        self.player = None
        self.avengers_list = self.create_avengers()
        self.locations = self.create_locations()
        self.active_spawns = []
    
    def create_avengers(self):
        """Create all available Avengers"""
        return [
            Avenger("Iron Man", "Legendary", 95, "city"),
            Avenger("Captain America", "Legendary", 90, "city"),
            Avenger("Thor", "Legendary", 98, "mountain"),
            Avenger("Hulk", "Legendary", 100, "forest"),
            Avenger("Black Widow", "Rare", 75, "city"),
            Avenger("Hawkeye", "Rare", 70, "forest"),
            Avenger("Spider-Man", "Rare", 80, "city"),
            Avenger("Black Panther", "Rare", 85, "forest"),
            Avenger("Doctor Strange", "Legendary", 92, "mountain"),
            Avenger("Scarlet Witch", "Legendary", 94, "mountain"),
            Avenger("Vision", "Rare", 88, "city"),
            Avenger("Ant-Man", "Common", 65, "park"),
            Avenger("Wasp", "Common", 68, "park"),
            Avenger("War Machine", "Rare", 82, "city"),
            Avenger("Falcon", "Common", 70, "park"),
        ]
    
    def create_locations(self):
        """Create game locations"""
        return [
            Location("Stark Tower", 40.7589, -73.9851, "city"),
            Location("Central Park", 40.7829, -73.9654, "park"),
            Location("Avengers Compound", 41.3113, -73.9246, "city"),
            Location("Wakanda Forest", 40.5, -74.2, "forest"),
            Location("Asgard Mountains", 41.0, -74.5, "mountain"),
        ]
    
    def start_game(self):
        """Initialize the game"""
        print("=" * 60)
        print("🦸 WELCOME TO AVENGERS GO! 🦸")
        print("=" * 60)
        print("Collect all the Avengers by exploring different locations!")
        print()
        
        name = input("Enter your hero name: ")
        self.player = Player(name)
        print(f"\n👋 Welcome, {self.player.name}!")
        print(f"📍 Starting location: New York City")
        print()
        
        self.spawn_avengers()
        self.game_loop()
    
    def spawn_avengers(self):
        """Spawn Avengers at nearby locations"""
        self.active_spawns = []
        for location in self.locations:
            if self.player.distance_to(location) < 0.5:
                # Spawn avengers matching location type
                matching_avengers = [a for a in self.avengers_list if a.location_type == location.location_type and not a.caught]
                if matching_avengers:
                    spawn_count = random.randint(1, 3)
                    for _ in range(spawn_count):
                        avenger = random.choice(matching_avengers)
                        self.active_spawns.append((avenger, location))
    
    def game_loop(self):
        """Main game loop"""
        while True:
            print("\n" + "=" * 60)
            print(f"⚡ Level {self.player.level} | XP: {self.player.experience} | Energy: {self.player.energy}/100")
            print(f"📦 Collection: {len(self.player.collection)}/{len(self.avengers_list)} Avengers")
            print("=" * 60)
            print("\n🗺️  MENU:")
            print("1. 🔍 Scan for nearby Avengers")
            print("2. 🚶 Move to a location")
            print("3. 🎯 Attempt to catch an Avenger")
            print("4. 📋 View your collection")
            print("5. 😌 Rest (restore energy)")
            print("6. 🚪 Quit game")
            
            choice = input("\nChoose an action (1-6): ")
            
            if choice == '1':
                self.scan_area()
            elif choice == '2':
                self.move_player()
            elif choice == '3':
                self.catch_avenger()
            elif choice == '4':
                self.view_collection()
            elif choice == '5':
                self.player.rest()
            elif choice == '6':
                print(f"\n👋 Thanks for playing, {self.player.name}!")
                print(f"Final collection: {len(self.player.collection)}/{len(self.avengers_list)} Avengers")
                break
            else:
                print("❌ Invalid choice!")
            
            time.sleep(0.5)
    
    def scan_area(self):
        """Scan for nearby Avengers"""
        print("\n🔍 Scanning area...")
        time.sleep(1)
        
        self.spawn_avengers()
        
        if not self.active_spawns:
            print("❌ No Avengers nearby. Try moving to a different location!")
            return
        
        print(f"\n✅ Found {len(self.active_spawns)} Avenger(s) nearby:")
        for i, (avenger, location) in enumerate(self.active_spawns, 1):
            print(f"  {i}. {avenger} at {location}")
    
    def move_player(self):
        """Move player to a new location"""
        print("\n🗺️  Available locations:")
        for i, loc in enumerate(self.locations, 1):
            distance = self.player.distance_to(loc)
            print(f"  {i}. {loc} - Distance: {distance:.2f}km")
        
        print("\nOr use WASD to move:")
        print("  W - North, S - South, A - West, D - East")
        
        choice = input("\nEnter location number or direction (w/a/s/d): ").lower()
        
        if choice in ['w', 'a', 's', 'd']:
            direction_map = {'w': 'n', 'a': 'w', 's': 's', 'd': 'e'}
            if self.player.move(direction_map[choice], 1):
                self.spawn_avengers()
        elif choice.isdigit() and 1 <= int(choice) <= len(self.locations):
            target = self.locations[int(choice) - 1]
            distance = self.player.distance_to(target)
            energy_cost = int(distance * 20)
            
            if self.player.energy >= energy_cost:
                self.player.lat = target.lat
                self.player.lon = target.lon
                self.player.energy -= energy_cost
                print(f"✅ Traveled to {target.name}! Energy: {self.player.energy}/100")
                self.spawn_avengers()
            else:
                print(f"❌ Not enough energy! Need {energy_cost}, have {self.player.energy}")
        else:
            print("❌ Invalid choice!")
    
    def catch_avenger(self):
        """Attempt to catch an Avenger"""
        if not self.active_spawns:
            print("\n❌ No Avengers nearby! Scan the area first.")
            return
        
        print("\n🎯 Available Avengers to catch:")
        for i, (avenger, location) in enumerate(self.active_spawns, 1):
            print(f"  {i}. {avenger}")
        
        choice = input("\nChoose an Avenger to catch (number): ")
        
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.active_spawns):
            print("❌ Invalid choice!")
            return
        
        avenger, location = self.active_spawns[int(choice) - 1]
        
        print(f"\n⚔️  Attempting to catch {avenger.name}...")
        time.sleep(1)
        
        # Catch probability based on rarity and player level
        base_chance = 0.7
        if avenger.rarity == "Rare":
            base_chance = 0.5
        elif avenger.rarity == "Legendary":
            base_chance = 0.3
        
        # Level bonus
        catch_chance = min(0.95, base_chance + (self.player.level * 0.05))
        
        if random.random() < catch_chance:
            print(f"🎉 SUCCESS! You caught {avenger.name}!")
            avenger.caught = True
            self.player.add_avenger(avenger)
            self.active_spawns.remove((avenger, location))
        else:
            print(f"💨 {avenger.name} escaped! Try again.")
    
    def view_collection(self):
        """Display player's collection"""
        print("\n" + "=" * 60)
        print("📦 YOUR AVENGERS COLLECTION")
        print("=" * 60)
        
        if not self.player.collection:
            print("Your collection is empty. Go catch some Avengers!")
            return
        
        for i, avenger in enumerate(self.player.collection, 1):
            print(f"{i}. {avenger}")
        
        total_power = sum(a.power_level for a in self.player.collection)
        print(f"\n💪 Total Team Power: {total_power}")

# Run the game
if __name__ == "__main__":
    game = AvengersGO()
    game.start_game()

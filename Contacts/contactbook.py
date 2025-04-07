import json

class Contact:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"👤 Name: {self.name}, 📞 Phone: {self.phone}, 📧 Email: {self.email}"

class ContactBook:
    def __init__(self):
        self.contacts: dict[str, Contact] = {}

    def add_contact(self, name: str, phone: str, email: str):
        if name in self.contacts:
            print(f"⚠️ Contact '{name}' already exists!")
            return
        self.contacts[name] = Contact(name, phone, email)
        print(f"✅ Contact '{name}' added successfully!")

    def view_contacts(self):
        if not self.contacts:
            print("📭 No contacts found!")
        else:
            print("📒 Contact List:")
            for contact in self.contacts.values():
                print(f"  - {contact}")

    def search_contact(self, name: str):
        contact = self.contacts.get(name)
        if contact:
            print(f"🔍 Found: {contact}")
        else:
            self._not_found(name)

    def update_contact(self, name: str, phone: str = None, email: str = None):
        contact = self.contacts.get(name)
        if contact:
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            print(f"✅ Contact '{name}' updated successfully!")
        else:
            self._not_found(name)

    def delete_contact(self, name: str):
        if name in self.contacts:
            del self.contacts[name]
            print(f"🗑️ Contact '{name}' deleted successfully!")
        else:
            self._not_found(name)

    def save_to_file(self, filename: str = "contacts.json"):
        try:
            with open(filename, "w") as file:
                json.dump({name: vars(contact) for name, contact in self.contacts.items()}, file, indent=4)
            print("💾 Contacts saved to file successfully!")
        except Exception as e:
            print(f"❌ Failed to save contacts: {e}")

    def load_from_file(self, filename: str = "contacts.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.contacts = {name: Contact(**info) for name, info in data.items()}
            print("📂 Contacts loaded from file successfully!")
        except FileNotFoundError:
            print("❌ No saved contacts found!")
        except Exception as e:
            print(f"❌ Failed to load contacts: {e}")

    def _not_found(self, name: str):
        print(f"❌ Contact '{name}' not found!")

def main():
    contact_book = ContactBook()
    
    # Optional: Allow user to specify a file or use default
    default_file = "contacts.json"
    contact_book.load_from_file(default_file)

    while True:
        print("\n📖 Contact Book Menu")
        print("======================")
        print("1️⃣  Add Contact")
        print("2️⃣  View Contacts")
        print("3️⃣  Search Contact")
        print("4️⃣  Update Contact")
        print("5️⃣  Delete Contact")
        print("6️⃣  Save & Exit")
        print("======================")
        
        choice = input("👉 Choose an option (1-6): ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()
            contact_book.add_contact(name, phone, email)

        elif choice == "2":
            contact_book.view_contacts()

        elif choice == "3":
            name = input("Enter name to search: ").strip()
            contact_book.search_contact(name)

        elif choice == "4":
            name = input("Enter name to update: ").strip()
            phone = input("Enter new phone (leave blank to keep unchanged): ").strip()
            email = input("Enter new email (leave blank to keep unchanged): ").strip()
            contact_book.update_contact(name, phone if phone else None, email if email else None)

        elif choice == "5":
            name = input("Enter name to delete: ").strip()
            contact_book.delete_contact(name)

        elif choice == "6":
            contact_book.save_to_file(default_file)
            print("👋 Exiting Contact Book. Have a great day!")
            break

        else:
            print("❌ Invalid option! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()

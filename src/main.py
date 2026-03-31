from github_api import get_all_data
from builder import generate_readme

def main():
    print("Fetching all GitHub and Static data...")
    # This single call grabs everything!
    all_data = get_all_data() 
    
    print("Generating new README.md...")
    # Pass the massive data dictionary to your builder
    generate_readme(all_data) 
    
    print("Successfully updated README!")

if __name__ == "__main__":
    main()
from sqlalchemy import create_engine, MetaData, Table, inspect, text
from app.connection_to_pg import DatabaseConnection
from sqlalchemy.orm import sessionmaker
from app.models.products import Product

def categorize_products():
    # Get database configuration
    db = DatabaseConnection()
    
    # Create a database URL
    db_url = f"postgresql://{db.db_config['user']}:{db.db_config['password']}@{db.db_config['host']}:{db.db_config['port']}/{db.db_config['database']}"
    
    # Create an engine and session
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Get all products
        products = session.query(Product).all()
        
        # Define category mapping (you can customize this based on your product names)
        category_mapping = {
            'laptop': 'Electronics',
            'phone': 'Electronics',
            'tablet': 'Electronics',
            'monitor': 'Electronics',
            'keyboard': 'Accessories',
            'mouse': 'Accessories',
            'headphones': 'Accessories',
            # Add more mappings as needed
        }

        # Update categories
        for product in products:
            # Convert product name to lowercase for case-insensitive matching
            name_lower = product.name.lower()
            
            # Find the first matching category
            category = None
            for key, value in category_mapping.items():
                if key in name_lower:
                    category = value
                    break
            
            # If no category found, set a default
            if not category:
                category = 'Other'
                
            product.category = category
        
        # Commit the changes
        session.commit()
        print(f"Updated categories for {len(products)} products")
        
        # Print a summary
        from collections import defaultdict
        category_counts = defaultdict(int)
        for p in session.query(Product).all():
            category_counts[p.category] += 1
        
        print("\nCategory distribution:")
        for category, count in category_counts.items():
            print(f"- {category}: {count} products")

    except Exception as e:
        print(f"Error updating categories: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    categorize_products()
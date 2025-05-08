# Libraries
import os
from hyperbrowser import Hyperbrowser
from hyperbrowser.models import StartBrowserUseTaskParams
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

hb_client = Hyperbrowser(api_key=os.getenv("HYPERBROWSER_API_KEY"))

def main():
    merchant_url = os.getenv("MERCHANT_URL")
    product_name = os.getenv("PRODUCT_NAME")
    customer_info = {
        "name": os.getenv("CUSTOMER_NAME"),
        "email": os.getenv("CUSTOMER_EMAIL"),
        "phone": os.getenv("CUSTOMER_PHONE"),
        "address": os.getenv("CUSTOMER_ADDRESS"),
        "city": os.getenv("CUSTOMER_CITY"),
        "state": os.getenv("CUSTOMER_STATE"),
        "zip": os.getenv("CUSTOMER_ZIP"),
        "country": os.getenv("CUSTOMER_COUNTRY"),
        "card_number": os.getenv("CUSTOMER_CARD_NUMBER"),
        "card_expiry": os.getenv("CUSTOMER_CARD_EXPIRY"),
        "card_cvv": os.getenv("CUSTOMER_CARD_CVV"),
    }

    session = hb_client.sessions.create()

    try:

        resp = hb_client.agents.browser_use.start_and_wait(
            StartBrowserUseTaskParams(
                # Prompt Instructions For Automation
                task=f"""
            ### Checkout Automation Task
    
            **Objective:**
            Visit {merchant_url}, find {product_name}, add it to cart, and complete the checkout process.
    
            **Steps:**
    
            1. Navigate to the merchant website: {merchant_url}
    
            2. Search for the product: "{product_name}"
               - Use the search functionality on the website
               - Look for exact or closest match to the specified product
    
            3. Select the product
               - Click on the product to view details if necessary
               - Select any required options (size, color, etc.)
    
            4. Add the product to cart
               - Analyze the product details to determine the appropriate add to cart button 
               - Click the "Add to Cart" button (or equivalent)
    
            5. Navigate to checkout/cart
               - Scroll to the top of the webpage and click on the cart, or similar button
               - Go through the steps necessary until you reach the checkout/fill in info page
               - If any info fill-in boxes are drop downs, select the appropriate dropdown option correlating to the data
    
            6. Fill in customer information using these details:
               - Full Name: {customer_info['name']}
               - Email: {customer_info['email']}
               - Phone: {customer_info['phone']}
    
            7. Fill in shipping address:
               - Address: {customer_info['address']}
               - City: {customer_info['city']}
               - State/Province: {customer_info['state']}
               - ZIP/Postal Code: {customer_info['zip']}
               - Country: {customer_info['country']}
    
            8. Continue to the checkout. Select shipping method (choose standard)
    
            9. Fill in payment details if required:
               - Credit Card: {customer_info['card_number']}
               - Expiration Date: {customer_info['card_expiry']}
               - CVV: {customer_info['card_cvv']}
    
            10. Review order details before final submission, make sure that you check the box that billing address is the same as shipping address if needed.
    
            11. Complete the order (or stop before final payment submission if this is a test) *This is a test*
            """,

            session_id = session.id,
            keep_browser_open = True,
            )
        )

        print("\nCheckout Result:")
        print(resp)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        hb_client.sessions.stop(session.id)


if __name__ == "__main__":
    try:
        main()
        print("Checkout Process Complete.")
    except Exception as e:
        print(f"Error: {e}")


# Libraries
import os
import asyncio
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
import logging

load_dotenv()

from hyperbrowser_agent import Hyperbrowser

from langchain_openai import ChatOpenAI as LLM
model= "gpt-4.1"

async def run_checkout():

    config = BrowserConfig(headless=False)

    browser = Browser(config=config)

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

    # Prompt Instructions For Automation
    task = f"""
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
    """

    # Initialize The AI Agent
    agent = Agent(
        task = task,
        llm = LLM(model_name=model),
        browser = browser,
    )

    try:
        # Run The AI Agent
        print(f"starting checkout process for {product_name} at {merchant_url}.")
        result = await agent.run()
        print("checkout process complete.")
        return result
    finally:
        await browser.close()

    result = run_checkout_agent(merchant_url, product_name, customer_info)
    print("/nCheckout Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(run_checkout())


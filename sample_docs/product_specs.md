# ShopSmart Product Specifications

This document describes the functional and test relevant details for the three products shown on the checkout page.

## P1001 Noise Canceling Headphones

- Name inside UI: `Noise Canceling Headphones`
- Element id: `product-name-1`
- Default quantity id: `quantity-1`
- Price text id: `price-1`
- Base price: ₹4,999
- Available color: Black
- Model: NCX100
- Cart quantity allowed: 0 to 5
- Typical test cases:
  - Increase and decrease quantity
  - Verify price formatting
  - Validate that total reflects quantity changes

## P1002 Mechanical Keyboard

- Name inside UI: `Mechanical Keyboard`
- Element id: `product-name-2`
- Default quantity id: `quantity-2`
- Price text id: `price-2`
- Base price: ₹3,299
- Switch type: Blue switches
- Layout: Compact 75 percent
- Cart quantity allowed: 0 to 5

## P1003 USB C Docking Station

- Name inside UI: `USB C Docking Station`
- Element id: `product-name-3`
- Default quantity id: `quantity-3`
- Price text id: `price-3`
- Base price: ₹2,499
- Ports: HDMI, USB A, USB C, Ethernet
- Cart quantity allowed: 0 to 5

## Currency and formatting rules

- All prices are shown in Indian Rupees with a currency symbol and comma separation.
- The total section uses these element ids:
  - Subtotal: `summary-subtotal`
  - Tax: `summary-tax`
  - Shipping: `summary-shipping`
  - Discount: `summary-discount`
  - Total: `summary-total`
- UI always displays totals as read only labels for automation validation.

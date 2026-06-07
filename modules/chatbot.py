import json, os, re
from openai import OpenAI
from dotenv import load_dotenv


class FashionChatbot:

    def __init__(self):
        self.client   = OpenAI(api_key=self._get_key())
        self.products = self._load("data/products.json")
        self.orders   = self._load("data/orders.json")
        self.faqs     = self._load("data/faqs.json")
        self.history  = []

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _get_key(self):
        try:
            import streamlit as st
            return st.secrets["OPENAI_API_KEY"]
        except Exception:
            load_dotenv()
            return os.getenv("OPENAI_API_KEY")

    def _load(self, path):
        with open(path) as f:
            return json.load(f)

    # ── System prompt ──────────────────────────────────────────────────────────

    def _system_prompt(self):
        faq_block = "\n".join(
            f"Q: {f['question']}\nA: {f['answer']}" for f in self.faqs
        )
        product_block = "\n".join(
            f"- {p['name']} | {p['category']} | "
            f"£{p['sale_price'] if p['sale_price'] else p['price']} | "
            f"Colors: {', '.join(p['colors'])} | "
            f"Sizes: {', '.join(p['sizes'])} | "
            f"Rating: {p['rating']}/5 | ID: {p['id']}"
            for p in self.products
        )
        return f"""You are StyleBot, a smart and friendly AI customer support assistant for StyleAI — a premium Fashion & Clothing e-commerce store.

You help customers with:
- Product info, sizing, and stock availability
- Order tracking and status updates
- Shipping, returns, and exchange policies
- Personalised outfit and product recommendations
- General store FAQs

LIVE PRODUCT CATALOG:
{product_block}

STORE POLICIES & FAQs:
{faq_block}

GUIDELINES:
- Be warm, concise, and fashion-savvy
- For order tracking: if no order ID given, ask for it (format ORD-XXXXX)
- For recommendations: ask about style preference, occasion, budget, or color if not mentioned
- Highlight sale prices when available
- Mention ratings for recommended products
- Never make up products or policies not in the data above
- End replies with a relevant follow-up question to keep the conversation going
"""

    # ── Intent detection ───────────────────────────────────────────────────────

    def _detect_intent(self, msg):
        m = msg.lower()
        if any(k in m for k in ["track", "order", "ord-", "status",
                                 "where is my", "shipped", "delivery", "dispatch"]):
            return "order_tracking"
        if any(k in m for k in ["return", "refund", "exchange",
                                 "wrong item", "wrong size", "send back"]):
            return "returns"
        if any(k in m for k in ["recommend", "suggest", "looking for",
                                 "need a", "want a", "find me", "outfit",
                                 "what should i wear", "gift"]):
            return "recommendation"
        if any(k in m for k in ["size", "sizing", "fit",
                                 "measurements", "bust", "waist", "hips", "cm"]):
            return "sizing"
        if any(k in m for k in ["ship", "shipping", "deliver",
                                 "how long", "international", "free shipping"]):
            return "shipping"
        return "general"

    # ── Order data injection ───────────────────────────────────────────────────

    def _inject_order_data(self, msg):
        match = re.search(r'ORD-\d+', msg.upper())
        if not match:
            return ""
        oid   = match.group()
        order = next((o for o in self.orders if o["order_id"] == oid), None)
        if not order:
            return f"\n[SYSTEM: Order {oid} was not found in the database.]"
        items_str = ", ".join(
            f"{i['product']} (Size: {i['size']}, Color: {i['color']}, Qty: {i['qty']})"
            for i in order["items"]
        )
        tracking  = order.get("tracking") or "Not yet assigned"
        delivered = order.get("delivered_on") or "Pending"
        refund    = order.get("refund_status", "")
        return (
            f"\n[SYSTEM ORDER DATA — use this to answer the customer]:\n"
            f"Order ID: {order['order_id']} | Status: {order['status']} | "
            f"Customer: {order['customer']} | Date: {order['date']} | "
            f"Items: {items_str} | Total: £{order['total']} | "
            f"Tracking: {tracking} | Est. Delivery: {order['estimated_delivery']} | "
            f"Delivered On: {delivered}"
            + (f" | Refund Status: {refund}" if refund else "")
        )

    # ── Product matching ───────────────────────────────────────────────────────

    def _matched_products(self, reply_text):
        found = []
        for p in self.products:
            if p["name"].lower() in reply_text.lower():
                found.append(p)
        return found[:3]

    # ── Main chat ──────────────────────────────────────────────────────────────

    def chat(self, user_message):
        intent    = self._detect_intent(user_message)
        order_ctx = self._inject_order_data(user_message)
        full_msg  = user_message + order_ctx

        self.history.append({"role": "user", "content": full_msg})

        messages = [{"role": "system", "content": self._system_prompt()}] + self.history

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})

        return {
            "reply":    reply,
            "intent":   intent,
            "tokens":   response.usage.total_tokens,
            "products": self._matched_products(reply) if intent == "recommendation" else []
        }

    # ── Reset ──────────────────────────────────────────────────────────────────

    def reset(self):
        self.history = []
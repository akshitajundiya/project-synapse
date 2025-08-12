import random

def check_traffic(location: str = None, route_id: str = None):
    """Simulate checking traffic conditions."""
    loc_info = {}
    if location:
        loc_info["location"] = location
    if route_id:
        loc_info["route_id"] = route_id
    if not loc_info:
        loc_info["location"] = "unknown"
    return {
        "location": loc_info,
        "traffic_level": random.choice(["low", "moderate", "heavy"]),
        "eta_min": random.randint(5, 45)
    }

def get_merchant_status(merchant_id: str = None):
    """Simulate retrieving merchant status."""
    if not merchant_id:
        return {"error": "merchant_id_missing"}
    return {
        "merchant_id": merchant_id,
        "open": True,
        "prep_time_min": random.randint(10, 50),
        "queue_len": random.randint(0, 5),
        "note": "Operational"
    }

def get_nearby_merchants(merchant_id: str = None, radius_km: float = 2.0):
    """Simulate finding nearby merchants."""
    if not merchant_id:
        return {"error": "merchant_id_missing"}
    return {
        "merchant_id": merchant_id,
        "radius_km": radius_km,
        "alternatives": [
            {"id": merchant_id + "_alt1", "prep_time_min": 15},
            {"id": merchant_id + "_alt2", "prep_time_min": 20}
        ]
    }

def re_route_driver(driver_id: str = None, new_location: str = None):
    """Simulate re-routing a driver."""
    return {"driver_id": driver_id, "rerouted_to": new_location, "status": "success"}

def notify_customer(customer_id: str = None, message: str = ""):
    """Simulate notifying a customer."""
    return {"customer_id": customer_id, "message_sent": message}

def initiate_mediation_flow(order_id: str = None):
    """Simulate initiating mediation for a dispute."""
    return {"order_id": order_id, "mediation_started": True}

def collect_evidence(order_id: str = None):
    """Simulate evidence collection."""
    return {
        "order_id": order_id,
        "photos": ["photo1.jpg", "photo2.jpg"],
        "statements": ["driver statement", "customer statement"]
    }

def analyze_evidence(order_id: str = None):
    """Simulate evidence analysis."""
    return {
        "order_id": order_id,
        "fault": random.choice(["driver", "merchant", "customer"]),
        "confidence": round(random.uniform(0.5, 0.95), 2)
    }

def issue_instant_refund(order_id: str = None, amount: float = 0.0):
    """Simulate issuing a refund."""
    return {"order_id": order_id, "refund_amount": amount, "status": "processed"}

def exonerate_driver(driver_id: str = None):
    """Simulate clearing driver of fault."""
    return {"driver_id": driver_id, "status": "exonerated"}

def log_merchant_packaging_feedback(merchant_id: str = None, feedback: str = ""):
    """Simulate logging feedback for a merchant."""
    if not merchant_id:
        return {"error": "merchant_id_missing"}
    return {"merchant_id": merchant_id, "feedback_logged": feedback}

def contact_recipient_via_chat(recipient_id: str = None, message: str = ""):
    """Simulate contacting recipient via chat."""
    return {"recipient_id": recipient_id, "message_sent": message}

def find_nearby_locker(location: str = None):
    """Simulate finding a nearby parcel locker."""
    return {
        "location": location or "unknown",
        "lockers": [
            {"id": "locker1", "distance_km": 0.5},
            {"id": "locker2", "distance_km": 1.2}
        ]
    }

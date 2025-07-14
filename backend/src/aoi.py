from shapely.geometry import box

def get_bbox(area_key="gurgaon_south_delhi"):
    """
    Get bounding box for analysis area.
    
    Args:
        area_key: Area to analyze. Options:
            - "gurgaon_south_delhi" (default - maximum visible change)
            - "noida_greater_noida" (planned development)
            - "bangalore_electronic_city" (IT expansion)
            - "pune_hinjewadi" (tech hub)
            - "mumbai_navi_mumbai" (long-term development)
            - "hyderabad_cyberabad" (modern planning)
            - "chennai_omr" (coastal development)
            - "delhi_dwarka" (planned sub-city)
            - "ahmedabad_sanand" (industrial)
            - "kolkata_salt_lake" (wetland conversion)
    
    Returns:
        list: [min_lon, min_lat, max_lon, max_lat]
    """
    
    aoi_coordinates = {
        "gurgaon_south_delhi": [77.0, 28.4, 77.3, 28.7],  # Rapid urban expansion
        "noida_greater_noida": [77.3, 28.4, 77.7, 28.7],  # Planned development
        "bangalore_electronic_city": [77.6, 12.8, 77.9, 13.1],  # IT expansion
        "pune_hinjewadi": [73.6, 18.5, 73.8, 18.7],  # Tech hub
        "mumbai_navi_mumbai": [72.8, 19.0, 73.2, 19.3],  # Long-term development
        "hyderabad_cyberabad": [78.3, 17.4, 78.6, 17.6],  # Modern planning
        "chennai_omr": [80.2, 12.8, 80.4, 13.0],  # Coastal development
        "delhi_dwarka": [77.0, 28.5, 77.2, 28.7],  # Planned sub-city
        "ahmedabad_sanand": [72.3, 22.9, 72.7, 23.2],  # Industrial development
        "kolkata_salt_lake": [88.4, 22.5, 88.5, 22.6],  # Wetland conversion
        
        # Additional high-change areas
        "chennai_it_corridor": [80.1, 12.7, 80.3, 12.9],  # IT corridor
        "kochi_infopark": [76.3, 9.9, 76.4, 10.1],  # IT development
        "jaipur_mahindra_world_city": [76.6, 26.8, 76.8, 27.0],  # Planned city
        "coimbatore_tidel_park": [76.9, 10.9, 77.1, 11.1],  # IT park
        
        # Traditional high-change test areas
        "delhi_sample": [76.85, 28.60, 76.95, 28.70],  # Original sample area
        "mumbai_central": [72.8, 19.0, 72.9, 19.1],  # Dense urban
        "bangalore_central": [77.5, 12.9, 77.6, 13.0],  # Urban core
    }
    
    if area_key in aoi_coordinates:
        print(f"Using AOI: {area_key}")
        print(f"Coordinates: {aoi_coordinates[area_key]}")
        return aoi_coordinates[area_key]
    else:
        print(f"Area '{area_key}' not found. Available areas:")
        for key in aoi_coordinates.keys():
            print(f"  - {key}")
        print(f"Using default: gurgaon_south_delhi")
        return aoi_coordinates["gurgaon_south_delhi"]

def get_geometry(area_key="gurgaon_south_delhi"):
    """
    Get geometry for analysis area.
    
    Args:
        area_key: Area to analyze (same options as get_bbox)
    
    Returns:
        Shapely box geometry
    """
    return box(*get_bbox(area_key))

def get_area_info(area_key="gurgaon_south_delhi"):
    """
    Get detailed information about an analysis area.
    
    Args:
        area_key: Area to get information about
    
    Returns:
        dict: Area information including expected changes, best time periods, etc.
    """
    
    area_info = {
        "gurgaon_south_delhi": {
            "name": "Gurgaon-South Delhi Urban Expansion",
            "description": "Rapid urban expansion from Delhi into Gurgaon. Shows dramatic agricultural to urban conversion.",
            "expected_changes": "Significant NDVI decrease in urban expansion areas",
            "best_time_period": "2018-2024",
            "change_type": "Rapid urbanization",
            "difficulty": "Easy - very visible changes"
        },
        "noida_greater_noida": {
            "name": "Noida-Greater Noida Industrial Corridor", 
            "description": "Planned industrial and residential development east of Delhi.",
            "expected_changes": "Sharp NDVI boundaries between developed and undeveloped areas",
            "best_time_period": "2015-2024",
            "change_type": "Planned development",
            "difficulty": "Easy - clear boundaries"
        },
        "bangalore_electronic_city": {
            "name": "Bangalore Electronic City Expansion",
            "description": "IT corridor development south of Bangalore. Mix of tech parks and agricultural land.",
            "expected_changes": "Patchy NDVI changes due to mixed development",
            "best_time_period": "2010-2024",
            "change_type": "IT expansion",
            "difficulty": "Moderate - mixed patterns"
        },
        "pune_hinjewadi": {
            "name": "Pune-Hinjewadi IT Hub",
            "description": "Major IT hub development west of Pune. Rural to high-tech transformation.",
            "expected_changes": "Concentrated NDVI loss in IT development zones",
            "best_time_period": "2008-2024",
            "change_type": "Tech hub development",
            "difficulty": "Easy - concentrated changes"
        },
        "mumbai_navi_mumbai": {
            "name": "Mumbai-Navi Mumbai Corridor",
            "description": "Planned city development across Thane Creek. Urban expansion over mangroves.",
            "expected_changes": "Gradual NDVI decrease with infrastructure development",
            "best_time_period": "2000-2024",
            "change_type": "Long-term planned development",
            "difficulty": "Moderate - gradual changes"
        },
        "hyderabad_cyberabad": {
            "name": "Hyderabad-Cyberabad HITEC City",
            "description": "IT and biotechnology hub development. Rural areas transformed into tech corridors.",
            "expected_changes": "Clustered NDVI reduction around tech hubs",
            "best_time_period": "2005-2024",
            "change_type": "Tech sector development",
            "difficulty": "Easy - clear clusters"
        },
        "chennai_omr": {
            "name": "Chennai Old Mahabalipuram Road (OMR)",
            "description": "IT corridor along OMR. Agricultural and coastal areas developed for tech industry.",
            "expected_changes": "Linear NDVI changes along the corridor",
            "best_time_period": "2010-2024",
            "change_type": "Coastal urban development",
            "difficulty": "Easy - linear pattern"
        },
        "delhi_dwarka": {
            "name": "Delhi Dwarka Sub-City",
            "description": "Planned sub-city development in Delhi. Rural areas converted to residential zones.",
            "expected_changes": "Systematic NDVI reduction in developed sectors",
            "best_time_period": "2005-2024",
            "change_type": "Planned residential development",
            "difficulty": "Easy - systematic pattern"
        },
        "ahmedabad_sanand": {
            "name": "Ahmedabad-Sanand Industrial Belt",
            "description": "Major automobile manufacturing hub. Agricultural areas converted to industrial use.",
            "expected_changes": "Large-scale NDVI reduction in industrial zones",
            "best_time_period": "2010-2024",
            "change_type": "Industrial development",
            "difficulty": "Easy - large-scale changes"
        },
        "kolkata_salt_lake": {
            "name": "Kolkata Salt Lake-New Town",
            "description": "Planned township development on reclaimed wetlands.",
            "expected_changes": "Dramatic NDVI changes from wetland to urban",
            "best_time_period": "2000-2024",
            "change_type": "Wetland conversion",
            "difficulty": "Easy - dramatic changes"
        }
    }
    
    return area_info.get(area_key, {
        "name": "Unknown Area",
        "description": "Area information not available",
        "expected_changes": "Unknown",
        "best_time_period": "2020-2024",
        "change_type": "Unknown",
        "difficulty": "Unknown"
    })

def print_area_recommendations():
    """
    Print recommendations for area selection based on analysis goals.
    """
    print("=== AOI RECOMMENDATIONS FOR NDVI CHANGE DETECTION ===\n")
    
    print("🚀 FOR BEGINNERS (Easy, Dramatic Changes):")
    beginner_areas = ["gurgaon_south_delhi", "noida_greater_noida", "ahmedabad_sanand", "delhi_dwarka"]
    for area in beginner_areas:
        info = get_area_info(area)
        print(f"  • {area}: {info['name']}")
        print(f"    Expected: {info['expected_changes']}")
        print(f"    Best period: {info['best_time_period']}\n")
    
    print("🔬 FOR DETAILED ANALYSIS (Moderate Complexity):")
    moderate_areas = ["bangalore_electronic_city", "mumbai_navi_mumbai", "chennai_omr"]
    for area in moderate_areas:
        info = get_area_info(area)
        print(f"  • {area}: {info['name']}")
        print(f"    Expected: {info['expected_changes']}")
        print(f"    Best period: {info['best_time_period']}\n")
    
    print("🌍 FOR SPECIFIC RESEARCH INTERESTS:")
    print("  • IT Sector Impact: pune_hinjewadi, hyderabad_cyberabad, chennai_omr")
    print("  • Industrial Development: ahmedabad_sanand")
    print("  • Planned Cities: delhi_dwarka, mumbai_navi_mumbai")
    print("  • Wetland Conversion: kolkata_salt_lake")
    print("  • Coastal Development: chennai_omr, mumbai_navi_mumbai")
    
    print("\n📊 QUICK SELECTION GUIDE:")
    print("  ✅ Maximum visible change: gurgaon_south_delhi")
    print("  ✅ Clean boundaries: noida_greater_noida")
    print("  ✅ Long-term trends: mumbai_navi_mumbai")
    print("  ✅ Industrial focus: ahmedabad_sanand")
    print("  ✅ Tech sector: pune_hinjewadi")

if __name__ == "__main__":
    print_area_recommendations()
# Smart India Hackathon Workshop
# Date:26-10-2026
## Register Number:212224040278
## Name:RITHISH R
## Problem Title
SIH 1710: Enhancing Navigation for Railway Station Facilities and Locations
## Problem Description
Background: Railway stations are complex environments with numerous facilities and locations such as ticket counters, platforms, restrooms, food courts, and waiting areas. Passengers often face difficulties in navigating these spaces, especially in large or unfamiliar stations. Efficient and user-friendly navigation systems are crucial for improving passenger experience, reducing congestion, and ensuring timely travel connections. Description: The problem involves developing a comprehensive navigation solution for railway stations that assists passengers in locating various facilities and destinations within the station premises. This includes creating detailed maps, providing real-time directions, and integrating features such as accessibility options for individuals with disabilities. The solution should be intuitive, easy to use, and accessible via multiple platforms, including mobile devices and digital kiosks. Key challenges include updating navigation information in real-time, ensuring accuracy, and accommodating the diverse needs of all passengers. Expected Solution: The expected solution is a multi-platform navigation system that provides detailed, real-time directions to all facilities and locations within a railway station. This system should include: A mobile application with 3D interactive maps and step-by-step navigation. Digital kiosks located throughout the station with touch-screen interfaces. Voice-guided navigation for visually impaired passengers. Regular updates to reflect changes in station layout and facility locations. Integration with existing railway apps and services for seamless user experience. The solution should enhance the overall passenger experience by reducing confusion, saving time, and improving accessibility within the station.

## Problem Creater's Organization
Ministry of Railway

## Idea

RailNav AI – Smart Railway Station Navigation and Assistance System is a user-friendly navigation platform that helps passengers locate railway station facilities and reach their destinations efficiently using interactive maps, step-by-step directions, voice guidance, and accessible routes.


## Proposed Solution / Architecture Diagram

RailNav AI provides a web application that helps passengers find platforms, ticket counters, restrooms, food courts, waiting halls, lifts, and other facilities. It calculates suitable routes using Dijkstra’s algorithm or A* search and displays estimated walking distances and times. Voice guidance assists visually impaired passengers, while accessible routing helps wheelchair users find suitable paths. QR codes can identify indoor checkpoints, and an administrator dashboard allows facility and route information to be updated.
<img width="953" height="476" alt="image" src="https://github.com/user-attachments/assets/8c40d736-6237-4771-a5b8-77571a071f95" />


## Use Cases

1. Facility Search: Locate platforms, ticket counters, restrooms, food courts, and waiting areas.

2. Route Navigation: Receive step-by-step directions and estimated walking time.

3. Accessibility Support: Find wheelchair-friendly routes, lifts, and ramps.

4. Voice Assistance: Listen to spoken navigation instructions.

5. Indoor Location: Use QR codes to identify station checkpoints.

6. Station Management: Update facility locations and blocked routes.

7. Passenger Information: Display platform and facility updates when reliable data is available.

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: SQLite
- Mapping: Leaflet.js, OpenStreetMap
- Route Planning: Dijkstra’s algorithm, A* search
- Voice Assistance: Web Speech API
- Development Environment: Google Antigravity
- Version Control: Git and GitHub

## Dependencies

- Python 3.x and Flask
- SQLite database
- Leaflet.js and OpenStreetMap
- Station maps and facility-location data
- Route-planning algorithms and mapped pathways
- Browser support for text-to-speech
- QR codes and a camera or QR scanner
- Internet connectivity for online map resources
- Authorized railway APIs or data sources for real-time information, if available

## Expected Outcome

RailNav AI aims to reduce passenger confusion, save time, improve accessibility, and provide a convenient navigation experience within railway stations.

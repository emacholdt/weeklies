# Weeklies for Home Assistant 🗓️

<img src="https://raw.githubusercontent.com/emacholdt/weeklies/main/logo.svg" align="right" width="128" height="128" alt="Weeklies Logo">

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/emacholdt/weeklies.svg)](https://github.com/emacholdt/weeklies/releases)

**Weeklies** is a custom Home Assistant integration designed to help families manage weekly recurring tasks and reminders. 

Unlike a standard To-Do list where items disappear once checked, **Weeklies** is designed for things that happen *every week* (e.g., "Pack Gym Bag" on Mondays, "Take out Trash" on Tuesdays).

## ✨ Features

*   **📅 Weekly Lists**: Dedicated lists for every day of the week (Monday - Sunday).
*   **✅ Native Todo Support**: Integrates with Home Assistant's native Todo List UI for easy management.
*   **🤖 Automation Ready**: Exposes `sensor.weeklies_today` and `sensor.weeklies_tomorrow` for powerful automations.
*   **💾 Persistent**: Data is stored safely in Home Assistant and survives restarts.
*   **🎨 Icon Support**: Add icons to items (visible in sensor attributes) for custom dashboards.

## 📥 Installation

### Option 1: HACS (Recommended)
1.  Open HACS in Home Assistant.
2.  Go to **Integrations** > **Top right menu** > **Custom repositories**.
3.  Add `https://github.com/emacholdt/weeklies` with category **Integration**.
4.  Click **Install**.
5.  Restart Home Assistant.

### Option 2: Manual
1.  Download the latest release.
2.  Copy the `custom_components/weeklies` folder to your `config/custom_components/` directory.
3.  Restart Home Assistant.

## ⚙️ Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration**.
3.  Search for **Weeklies**.
4.  Follow the prompts to add it.

## 🚀 Usage

### In the Dashboard
Add a **Todo List** card to your dashboard and select one of the `Weeklies` lists (e.g., `Weeklies Monday`). You can add and remove items directly from the UI.

### In Automations
Use the `sensor.weeklies_today` sensor to trigger notifications.

```yaml
automation:
  - alias: "Morning Reminders"
    trigger:
      - platform: time
        at: "07:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.weeklies_today
        above: 0
    action:
      - service: notify.mobile_app_family
        data:
          message: "Don't forget today: {{ state_attr('sensor.weeklies_today', 'items') | map(attribute='text') | join(', ') }}"
```

## 📊 Dashboard Examples

### Dynamic Daily Card (Markdown)
This card automatically shows the tasks for the current day, including your custom icons. It's cleaner than the Todo card for a "read-only" view.

```yaml
type: markdown
content: >
  ## 📅 {{ now().strftime('%A') }}'s Tasks
  
  {% set items = state_attr('sensor.weeklies_today', 'items') %}
  {% if items %}
    {% for item in items %}
    - <ha-icon icon="{{ item.icon | default('mdi:checkbox-blank-circle-outline') }}"></ha-icon> {{ item.text }}
    {% endfor %}
  {% else %}
    *No tasks for today!* 🎉
  {% endif %}
```

```

### Morning Routine (Time-Based)
This card uses Jinja2 templates to only show content between **Midnight and 8:00 AM**.
*Note: To completely hide the card border when empty, wrap this in a [Conditional Card](https://www.home-assistant.io/dashboards/conditional/) linked to a [Time of Day](https://www.home-assistant.io/integrations/tod/) binary sensor.*

```yaml
type: markdown
content: >
  {% set current_hour = now().hour %}
  
  {% if current_hour < 8 %}
    ## 🌅 Morning Tasks
    
    {% set items = state_attr('sensor.weeklies_today', 'items') %}
    {% if items %}
      {% for item in items %}
      - <ha-icon icon="{{ item.icon | default('mdi:checkbox-blank-circle-outline') }}"></ha-icon> {{ item.text }}
      {% endfor %}
    {% else %}
      *No tasks for this morning.*
    {% endif %}
  {% endif %}
```

## 🛠️ Services

**`weeklies.add_item`**
Add an item with an optional icon (icons are visible in sensor attributes).
```yaml
service: weeklies.add_item
data:
  day: monday
  text: "Gym"
  icon: "mdi:dumbbell"
```

**`weeklies.remove_item`**
Remove an item.
```yaml
service: weeklies.remove_item
data:
  day: monday
  text: "Gym"
```

## ❤️ Contributing
Issues and Pull Requests are welcome!

## 📄 License
MIT License

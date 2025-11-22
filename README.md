# Weeklies for Home Assistant 🗓️

<img src="https://raw.githubusercontent.com/emacholdt/weeklies/main/logo.svg" align="right" width="128" height="128" alt="Weeklies Logo">

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/emacholdt/weeklies.svg)](https://github.com/emacholdt/weeklies/releases)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow.svg)](https://www.buymeacoffee.com/brusselssprites)

**Weeklies** is a custom Home Assistant integration designed to help families manage weekly recurring tasks and reminders. 

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
    <ha-icon icon="{{ item.icon | default('mdi:checkbox-blank-circle-outline') }}"></ha-icon> {{ item.text }}
    {% endfor %}
  {% else %}
    *No tasks for today!* 🎉
  {% endif %}
```

### Morning Routine (Conditional Card)
This example uses a [Conditional Card](https://www.home-assistant.io/dashboards/conditional/) to only show your morning tasks when a specific condition is met. This is cleaner because it completely hides the card (including borders) when not needed.

**Prerequisite:** You need a binary sensor that is "on" during the morning. You can easily create this in your `configuration.yaml`:

```yaml
# configuration.yaml
binary_sensor:
  - platform: tod
    name: Morning
    after: "05:00:00"
    before: "12:00:00"
```

**Card Configuration:**

```yaml
type: conditional
conditions:
  - entity: binary_sensor.morning # Replace with your Time of Day sensor
    state: "on"
card:
  type: markdown
  content: >
    ## 🌅 Morning Tasks
    
    {% set items = state_attr('sensor.weeklies_today', 'items') %}
    {% if items %}
      {% for item in items %}
    <ha-icon icon="{{ item.icon | default('mdi:checkbox-blank-circle-outline') }}"></ha-icon> {{ item.text }}
      {% endfor %}
    {% else %}
      *No tasks for this morning.*
    {% endif %}
```

### Advanced Dashboard Examples

#### Hide Completed Items
This card filters out items that have been marked as "completed" in the Todo list, showing only what's left to do.

```yaml
type: markdown
content: >
  ## 📝 To Do
  
  {% set items = state_attr('sensor.weeklies_today', 'items') %}
  {% if items %}
    {% for item in items %}
      {% if item.status != 'completed' %}
    <ha-icon icon="{{ item.icon | default('mdi:checkbox-blank-circle-outline') }}"></ha-icon> {{ item.text }}
      {% endif %}
    {% endfor %}
  {% else %}
    *No tasks found.*
  {% endif %}
```

#### Strikethrough Completed Items
This card shows all items but crosses out the ones that are completed.

```yaml
type: markdown
content: >
  ## 📝 Daily List
  
  {% set items = state_attr('sensor.weeklies_today', 'items') %}
  {% if items %}
    {% for item in items %}
      {% if item.status == 'completed' %}
    <ha-icon icon="mdi:checkbox-marked-circle-outline"></ha-icon> <s>{{ item.text }}</s>
      {% else %}
    <ha-icon icon="{{ item.icon | default('mdi:checkbox-blank-circle-outline') }}"></ha-icon> {{ item.text }}
      {% endif %}
    {% endfor %}
  {% else %}
    *No tasks found.*
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

## 📸 Screenshots

| Daily View | Morning Routine | Advanced Strikethrough |
|:---:|:---:|:---:|
| ![Daily View](images/daily_view.png) | ![Morning Routine](images/morning_routine.png) | ![Advanced Strikethrough](images/advanced_strikesthrough.png) |
| *Standard Markdown Card* | *Conditional Morning Card* | *Strikethrough Completed* |

## ❤️ Contributing
Issues and Pull Requests are welcome!

## 📄 License
MIT License

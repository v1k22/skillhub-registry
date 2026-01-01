---
metadata:
  name: "wezterm-dev-setup"
  version: "1.0.0"
  description: "Complete WezTerm terminal configuration for developers with theme switching, pane management, and productivity features"
  category: "terminal-configuration"
  tags: ["wezterm", "terminal", "productivity", "development", "configuration"]
  author: "v1k22"
---

# WezTerm Development Configuration

## Overview
This skill sets up a fully-featured WezTerm terminal configuration optimized for developers. It includes automatic light/dark theme switching, custom fonts, leader-key based navigation (tmux-style), pane splitting, and productivity shortcuts for a seamless development experience.

## User Requirements

**Edit the features below to customize your setup:**

- Auto-detect system appearance and switch between dark (ForestBlue) and light (iTerm2 Light Background) themes
- Different fonts for dark theme (Operator Mono Lig Light 11pt) and light theme (Iosevka NFM 12pt)
- Leader key (Ctrl+F) for tmux-style pane and tab management
- Mouse bindings: right-click paste, auto-copy on selection
- Window opacity at 95% with 10px padding
- Tab bar with index numbers, auto-hide when single tab
- Multiple shell support: PowerShell (default), WSL, Command Prompt
- Keyboard shortcuts for tab management, pane splitting, and navigation
- Performance optimizations: 60 FPS, WebGpu front-end, 5000 scrollback lines
- External secrets file support for managing tokens and API keys
- Custom tab bar colors with dark theme
- Disable window close confirmation prompts

## Steps

### 1. Create Main Configuration File

Create `.wezterm.lua` in your home directory:


local wezterm = require("wezterm")
local config = wezterm.config_builder()

-- Load secrets from external file
local function load_secrets()
    local secrets_file = wezterm.home_dir .. "\\.wezterm_secrets.lua"
    local ok, secrets = pcall(dofile, secrets_file)
    if ok then
        return secrets
    else
        wezterm.log_error("Failed to load secrets file: " .. secrets_file)
        return { tokens = {} }
    end
end

local secrets = load_secrets()


This initializes the configuration and sets up external secrets loading functionality.

### 2. Configure Theme Auto-Switching


-- Auto-detect system appearance and switch themes
local function scheme_for_appearance(appearance)
    if appearance:find("Dark") then
        return "ForestBlue"
    else
        return "iTerm2 Light Background"
    end
end

config.color_scheme = scheme_for_appearance(wezterm.gui.get_appearance())


This automatically switches between dark and light themes based on system appearance settings.

### 3. Set Font Configuration


local appearance = wezterm.gui.get_appearance()
if appearance:find("Dark") then
    config.font = wezterm.font("Operator Mono Lig Light", { weight = "Regular" })
    config.font_size = 11.0
else
    config.font = wezterm.font("Iosevka NFM", { weight = "Regular" })
    config.font_size = 12.0
end

config.font_rules = {
    {
        intensity = "Bold",
        italic = false,
        font = wezterm.font("Operator Mono Lig Light", { weight = "Regular" }),
    },
    {
        intensity = "Bold",
        italic = true,
        font = wezterm.font("Operator Mono Lig Light", { weight = "Regular", italic = true }),
    },
}

-- Better rendering for light themes
if not appearance:find("Dark") then
    config.freetype_load_target = "Normal"
    config.freetype_render_target = "HorizontalLcd"
end


Uses different fonts optimized for dark and light modes with improved rendering.

### 4. Configure Window and Tab Settings


config.window_background_opacity = 0.95
config.text_background_opacity = 1.0
config.window_padding = {
    left = 10,
    right = 10,
    top = 10,
    bottom = 10,
}

config.enable_tab_bar = true
config.hide_tab_bar_if_only_one_tab = true
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = false
config.show_tab_index_in_tab_bar = true
config.tab_max_width = 32


Sets window transparency and configures the tab bar for better visibility and usability.

### 5. Customize Tab Bar Colors


config.colors = {
    tab_bar = {
        background = "#1a1b26",
        active_tab = {
            bg_color = "#7aa2f7",
            fg_color = "#1a1b26",
            intensity = "Bold",
        },
        inactive_tab = {
            bg_color = "#24283b",
            fg_color = "#c0caf5",
        },
        inactive_tab_hover = {
            bg_color = "#414868",
            fg_color = "#c0caf5",
        },
    },
}

wezterm.on("format-tab-title", function(tab, tabs, panes, config, hover, max_width)
    local title = tab.active_pane.title
    local index = tab.tab_index + 1
    return {
        { Text = " " .. index .. ": " .. title .. " " },
    }
end)


Applies custom colors to tab bar elements and formats tab titles with index numbers.

### 6. Optimize Performance Settings


config.max_fps = 60
config.animation_fps = 1
config.front_end = "WebGpu"
config.webgpu_power_preference = "HighPerformance"
config.enable_scroll_bar = false
config.enable_wayland = false
config.scrollback_lines = 5000

config.default_cursor_style = "BlinkingBar"
config.cursor_blink_rate = 500


Optimizes performance for smooth operation and sets cursor preferences.

### 7. Configure Mouse Bindings


local act = wezterm.action

config.mouse_bindings = {
    {
        event = { Down = { streak = 1, button = "Right" } },
        mods = "NONE",
        action = act.PasteFrom("Clipboard"),
    },
    {
        event = { Up = { streak = 1, button = "Right" } },
        mods = "NONE",
        action = act.Nop,
    },
    {
        event = { Up = { streak = 1, button = "Left" } },
        mods = "NONE",
        action = act.CompleteSelectionOrOpenLinkAtMouseCursor("ClipboardAndPrimarySelection"),
    },
}

config.selection_word_boundary = " \t\n{}[]()\"'`"


Enables right-click paste and auto-copy on selection for improved workflow.

### 8. Set Default Shell and Launch Menu


config.default_prog = { "powershell.exe" }
config.exit_behavior = "Close"

config.launch_menu = {
    {
        label = "PowerShell",
        args = { "powershell.exe" },
    },
    {
        label = "WSL",
        args = { "wsl.exe", "~" },
    },
    {
        label = "Command Prompt",
        args = { "cmd.exe" },
    },
}


Configures PowerShell as default shell with quick access to other shells via launch menu.

### 9. Configure Leader Key


config.leader = { key = "f", mods = "CTRL", timeout_milliseconds = 1000 }
config.window_close_confirmation = "NeverPrompt"


Sets Ctrl+F as the leader key for tmux-style navigation and disables close confirmation dialogs.

### 10. Set Up Keyboard Shortcuts


config.keys = {
    -- Tab management
    { key = "t", mods = "CTRL|SHIFT", action = act.SpawnTab("CurrentPaneDomain") },
    { key = "w", mods = "CTRL|SHIFT", action = act.CloseCurrentTab({ confirm = false }) },
    { key = "l", mods = "CTRL|SHIFT", action = act.ShowLauncher },
    { key = "u", mods = "CTRL|SHIFT", action = act.SpawnCommandInNewTab({ args = { "wsl.exe" } }) },
    
    -- Tab navigation with Leader
    { key = "n", mods = "LEADER", action = act.ActivateTabRelative(1) },
    { key = "p", mods = "LEADER", action = act.ActivateTabRelative(-1) },
    
    -- Pane splitting with Leader
    { key = "h", mods = "LEADER", action = act.SplitVertical({ domain = "CurrentPaneDomain" }) },
    { key = "v", mods = "LEADER", action = act.SplitHorizontal({ domain = "CurrentPaneDomain" }) },
    
    -- Pane navigation
    { key = "h", mods = "CTRL|SHIFT", action = act.ActivatePaneDirection("Left") },
    { key = "l", mods = "CTRL|SHIFT|ALT", action = act.ActivatePaneDirection("Right") },
    { key = "k", mods = "CTRL|SHIFT", action = act.ActivatePaneDirection("Up") },
    { key = "j", mods = "CTRL|SHIFT", action = act.ActivatePaneDirection("Down") },
    
    -- Pane management with Leader
    { key = "x", mods = "LEADER", action = act.CloseCurrentPane({ confirm = true }) },
    { key = "z", mods = "LEADER", action = act.TogglePaneZoomState },
    
    -- Utilities
    { key = "p", mods = "CTRL|SHIFT", action = act.ActivateCommandPalette },
    { key = "f", mods = "CTRL|SHIFT", action = act.Search({ CaseSensitiveString = "" }) },
    { key = "[", mods = "LEADER", action = act.ActivateCopyMode },
    { key = "Space", mods = "CTRL|SHIFT", action = act.QuickSelect },
    { key = "r", mods = "CTRL|SHIFT", action = act.ReloadConfiguration },
}


Creates comprehensive keyboard shortcuts for tab management, pane operations, and utilities.

### 11. Add Secrets Selector (Optional)


-- Secrets selector shortcut
table.insert(config.keys, {
    key = "q",
    mods = "ALT",
    action = act.InputSelector({
        title = "🔑 Tokens & Secrets",
        choices = secrets.tokens,
        action = wezterm.action_callback(function(window, pane, id, label)
            if id then
                pane:send_text(id)
            end
        end),
        fuzzy = true,
        fuzzy_description = "Type to filter: ",
    }),
})


Enables Alt+Q shortcut to quickly access stored tokens and secrets.

### 12. Add Numeric Tab Switching


-- Numeric tab switching with Leader (1-9)
for i = 1, 9 do
    table.insert(config.keys, {
        key = tostring(i),
        mods = "LEADER",
        action = act.ActivateTab(i - 1),
    })
end

return config


Allows Leader + [1-9] to quickly jump to specific tabs.

### 13. Create Secrets File (Optional)

Create `.wezterm_secrets.lua` in your home directory:


return {
    tokens = {
        { label = "GitHub PAT", id = "ghp_your_token_here" },
        { label = "OpenAI API Key", id = "sk-your_key_here" },
        { label = "AWS Access Key", id = "AKIA_your_key_here" },
    }
}


Stores sensitive tokens and API keys securely outside the main configuration file.

## Expected Output

After completing these steps, you should have:

- `.wezterm.lua` configuration file in your home directory
- (Optional) `.wezterm_secrets.lua` file for secure token storage
- WezTerm terminal with:
  - Automatic theme switching based on system appearance
  - Optimized fonts for both dark and light modes
  - Leader key (Ctrl+F) for tmux-style operations
  - Tab management with keyboard shortcuts
  - Pane splitting and navigation
  - Right-click paste and auto-copy functionality
  - Quick shell launcher (Ctrl+Shift+L)
  - Performance-optimized settings

## Troubleshooting

### Fonts Not Loading

# Verify fonts are installed on your system
# Download and install missing fonts before using them in config


### Secrets File Not Found

-- Check that .wezterm_secrets.lua exists in home directory
-- Verify file path uses correct separator for your OS (\ for Windows, / for Unix)


### Leader Key Not Working

# Press Ctrl+F (leader key) first, then the command key
# Example: Ctrl+F, then h (splits pane vertically)
# Increase timeout_milliseconds if needed


### Theme Not Switching Automatically

-- Ensure your system appearance settings are properly configured
-- Restart WezTerm after changing system theme
-- Check wezterm.gui.get_appearance() returns correct value


## Related Skills
- `tmux-configuration` - Similar pane management concepts
- `terminal-productivity` - General terminal workflow optimization
- `font-installation` - Installing custom fonts for terminal use

## References
- [WezTerm Official Documentation](https://wezfurlong.org/wezterm/)
- [WezTerm Configuration Examples](https://wezfurlong.org/wezterm/config/files.html)
- [WezTerm Key Bindings Reference](https://wezfurlong.org/wezterm/config/keys.html)

---

## Example Configuration Reference

Below is the complete working example that implements all the features described above:

local wezterm = require("wezterm")
local config = wezterm.config_builder()

-- Load secrets from external file
local function load_secrets()
	local secrets_file = wezterm.home_dir .. "\\.wezterm_secrets.lua"
	local ok, secrets = pcall(dofile, secrets_file)
	if ok then
		return secrets
	else
		wezterm.log_error("Failed to load secrets file: " .. secrets_file)
		return { tokens = {} }
	end
end

local secrets = load_secrets()

-- Auto-detect system appearance and switch themes
local function scheme_for_appearance(appearance)
	if appearance:find("Dark") then
		return "ForestBlue"
	else
        return "iTerm2 Light Background" -- Light theme
	end
end

-- Color scheme (auto-switches based on system theme)
config.color_scheme = scheme_for_appearance(wezterm.gui.get_appearance())

-- Font configuration
local appearance = wezterm.gui.get_appearance()
if appearance:find("Dark") then
	config.font = wezterm.font("Operator Mono Lig Light", { weight = "Regular" })
	config.font_size = 11.0
else
	config.font = wezterm.font("Iosevka NFM", { weight = "Regular" })
	config.font_size = 12.0
end

config.font_rules = {
	{
		intensity = "Bold",
		italic = false,
		font = wezterm.font("Operator Mono Lig Light", { weight = "Regular" }),
	},
	{
		intensity = "Bold",
		italic = true,
		font = wezterm.font("Operator Mono Lig Light", { weight = "Regular", italic = true }),
	},
}

-- Better font rendering for light themes
if not appearance:find("Dark") then
	config.freetype_load_target = "Normal"
	config.freetype_render_target = "HorizontalLcd"
end

-- Window configuration
config.window_background_opacity = 0.95
config.text_background_opacity = 1.0 -- Changed from 0.3 for better text readability
config.window_padding = {
	left = 10,
	right = 10,
	top = 10,
	bottom = 10,
}

-- Tab bar
config.enable_tab_bar = true
config.hide_tab_bar_if_only_one_tab = true
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = false
config.show_tab_index_in_tab_bar = true
config.tab_max_width = 32

-- Hyperlink rules (make URLs clickable)
config.hyperlink_rules = wezterm.default_hyperlink_rules()

-- Tab bar colors for better visibility
config.colors = {
	tab_bar = {
		background = "#1a1b26", -- Darker opaque background for tab bar
		active_tab = {
			bg_color = "#7aa2f7",
			fg_color = "#1a1b26",
			intensity = "Bold",
		},
		inactive_tab = {
			bg_color = "#24283b",
			fg_color = "#c0caf5",
		},
		inactive_tab_hover = {
			bg_color = "#414868",
			fg_color = "#c0caf5",
		},
	},
}

-- Format tab titles with padding for better height
wezterm.on("format-tab-title", function(tab, tabs, panes, config, hover, max_width)
	local title = tab.active_pane.title
	local index = tab.tab_index + 1
	return {
		{ Text = " " .. index .. ": " .. title .. " " },
	}
end)

-- Performance
config.max_fps = 60 -- Reduced from 120 for stability
config.animation_fps = 1 -- Disable smooth animations
config.front_end = "WebGpu" -- Try WebGpu instead
config.webgpu_power_preference = "HighPerformance"
config.enable_scroll_bar = false
config.enable_wayland = false
config.scrollback_lines = 5000 -- Reduced scrollback

-- Cursor
config.default_cursor_style = "BlinkingBar"
config.cursor_blink_rate = 500

-- Scrollback
config.scrollback_lines = 10000

-- Define action variable for use throughout config
local act = wezterm.action

-- Mouse bindings - copy on select and right-click paste
config.mouse_bindings = {
	-- Right click pastes from clipboard
	{
		event = { Down = { streak = 1, button = "Right" } },
		mods = "NONE",
		action = act.PasteFrom("Clipboard"),
	},
	-- Disable default right-click behavior
	{
		event = { Up = { streak = 1, button = "Right" } },
		mods = "NONE",
		action = act.Nop,
	},
	-- Copy on select with left mouse button release
	{
		event = { Up = { streak = 1, button = "Left" } },
		mods = "NONE",
		action = act.CompleteSelectionOrOpenLinkAtMouseCursor("ClipboardAndPrimarySelection"),
	},
}

-- Copy to clipboard on selection
config.selection_word_boundary = " \t\n{}[]()\"'`"

-- Default shell (PowerShell)
config.default_prog = { "powershell.exe" } -- Windows PowerShell 5.1
config.exit_behavior = "Close" -- Close the pane without error dialog

-- Launch menu with multiple shell options
config.launch_menu = {
	{
		label = "PowerShell",
		args = { "powershell.exe" },
	},
	{
		label = "WSL",
		args = { "wsl.exe", "~" },
	},
	{
		label = "Command Prompt",
		args = { "cmd.exe" },
	},
}

-- Leader key (similar to tmux)
config.leader = { key = "f", mods = "CTRL", timeout_milliseconds = 1000 }

-- Disable window close confirmation
config.window_close_confirmation = "NeverPrompt"

-- Key bindings

config.keys = {
	-- Tab management
	{
		key = "t",
		mods = "CTRL|SHIFT",
		action = act.SpawnTab("CurrentPaneDomain"),
	},
	{
		key = "w",
		mods = "CTRL|SHIFT",
		action = act.CloseCurrentTab({ confirm = false }),
	},
	{
		key = "l",
		mods = "CTRL|SHIFT",
		action = act.ShowLauncher,
	},
	{
		key = "u",
		mods = "CTRL|SHIFT",
		action = act.SpawnCommandInNewTab({
			args = { "wsl.exe" },
		}),
	},

	-- Tab navigation with Leader
	{
		key = "n",
		mods = "LEADER",
		action = act.ActivateTabRelative(1),
	},
	{
		key = "p",
		mods = "LEADER",
		action = act.ActivateTabRelative(-1),
	},

	-- Pane splitting
	{
		key = "h",
		mods = "LEADER",
		action = act.SplitVertical({ domain = "CurrentPaneDomain" }),
	},
	{
		key = "v",
		mods = "LEADER",
		action = act.SplitHorizontal({ domain = "CurrentPaneDomain" }),
	},

	-- Pane navigation
	{
		key = "h",
		mods = "CTRL|SHIFT",
		action = act.ActivatePaneDirection("Left"),
	},
	{
		key = "l",
		mods = "CTRL|SHIFT|ALT",
		action = act.ActivatePaneDirection("Right"),
	},
	{
		key = "k",
		mods = "CTRL|SHIFT",
		action = act.ActivatePaneDirection("Up"),
	},
	{
		key = "j",
		mods = "CTRL|SHIFT",
		action = act.ActivatePaneDirection("Down"),
	},

	-- Pane management
	{
		key = "x",
		mods = "LEADER",
		action = act.CloseCurrentPane({ confirm = true }),
	},
	{
		key = "z",
		mods = "LEADER",
		action = act.TogglePaneZoomState,
	},

	-- Command palette & search
	{
		key = "p",
		mods = "CTRL|SHIFT",
		action = act.ActivateCommandPalette,
	},
	{
		key = "f",
		mods = "CTRL|SHIFT",
		action = act.Search({ CaseSensitiveString = "" }),
	},
	{
		key = "[",
		mods = "LEADER",
		action = act.ActivateCopyMode,
	},

	-- Quick select & utilities
	{
		key = "Space",
		mods = "CTRL|SHIFT",
		action = act.QuickSelect,
	},
	{
		key = "u",
		mods = "CTRL|SHIFT|ALT",
		action = act.CharSelect,
	},
	{
		key = "r",
		mods = "CTRL|SHIFT",
		action = act.ReloadConfiguration,
	},

	-- Secrets selector
	{
		key = "q",
		mods = "ALT",
		action = act.InputSelector({
			title = "🔑 Tokens & Secrets",
			choices = secrets.tokens,
			action = wezterm.action_callback(function(window, pane, id, label)
				if id then
					pane:send_text(id)
				end
			end),
			fuzzy = true,
			fuzzy_description = "Type to filter: ",
		}),
	},
}

-- Numeric tab switching with Leader key (1-9)
for i = 1, 9 do
	table.insert(config.keys, {
		key = tostring(i),
		mods = "LEADER",
		action = act.ActivateTab(i - 1),
	})
end

return config
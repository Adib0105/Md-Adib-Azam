<?php
/**
 * Plugin Name: Restaurant Menu Manager
 * Description: Renders structured restaurant menu items.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_07_restaurant_menu_manager_render($attributes = []) {
    $attributes = shortcode_atts([
        'item' => '',
        'category' => '',
        'price' => ''
    ], $attributes, 'adib_07_restaurant-menu-manager');
    $html = '<section class="adib_07_restaurant_menu_manager-component"><h2>Restaurant Menu Manager</h2><dl>';
    if ($attributes['item'] !== '') { $html .= '<dt>Item</dt><dd>' . esc_html($attributes['item']) . '</dd>'; }
    if ($attributes['category'] !== '') { $html .= '<dt>Category</dt><dd>' . esc_html($attributes['category']) . '</dd>'; }
    if ($attributes['price'] !== '') { $html .= '<dt>Price</dt><dd>' . esc_html($attributes['price']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_07_restaurant-menu-manager', 'adib_07_restaurant_menu_manager_render');

function adib_07_restaurant_menu_manager_assets() {
    $css = '.adib_07_restaurant_menu_manager-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_07_restaurant_menu_manager-component label{display:block;margin:.8rem 0}'
         . '.adib_07_restaurant_menu_manager-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_07_restaurant_menu_manager-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_07_restaurant_menu_manager-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_07_restaurant_menu_manager', false, [], '1.0.0');
    wp_enqueue_style('adib_07_restaurant_menu_manager');
    wp_add_inline_style('adib_07_restaurant_menu_manager', $css);
}
add_action('wp_enqueue_scripts', 'adib_07_restaurant_menu_manager_assets');

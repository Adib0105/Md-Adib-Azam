<?php
/**
 * Plugin Name: Local Directory Cards
 * Description: Renders a local directory card collection.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_23_local_directory_cards_render($attributes = []) {
    $attributes = shortcode_atts([
        'business' => '',
        'category' => '',
        'location' => ''
    ], $attributes, 'adib_23_local-directory-cards');
    $html = '<section class="adib_23_local_directory_cards-component"><h2>Local Directory Cards</h2><dl>';
    if ($attributes['business'] !== '') { $html .= '<dt>Business</dt><dd>' . esc_html($attributes['business']) . '</dd>'; }
    if ($attributes['category'] !== '') { $html .= '<dt>Category</dt><dd>' . esc_html($attributes['category']) . '</dd>'; }
    if ($attributes['location'] !== '') { $html .= '<dt>Location</dt><dd>' . esc_html($attributes['location']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_23_local-directory-cards', 'adib_23_local_directory_cards_render');

function adib_23_local_directory_cards_assets() {
    $css = '.adib_23_local_directory_cards-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_23_local_directory_cards-component label{display:block;margin:.8rem 0}'
         . '.adib_23_local_directory_cards-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_23_local_directory_cards-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_23_local_directory_cards-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_23_local_directory_cards', false, [], '1.0.0');
    wp_enqueue_style('adib_23_local_directory_cards');
    wp_add_inline_style('adib_23_local_directory_cards', $css);
}
add_action('wp_enqueue_scripts', 'adib_23_local_directory_cards_assets');

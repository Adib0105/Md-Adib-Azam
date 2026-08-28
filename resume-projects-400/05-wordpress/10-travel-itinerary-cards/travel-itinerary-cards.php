<?php
/**
 * Plugin Name: Travel Itinerary Cards
 * Description: Renders a day-by-day travel itinerary.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_10_travel_itinerary_cards_render($attributes = []) {
    $attributes = shortcode_atts([
        'place' => '',
        'day' => '',
        'activity' => ''
    ], $attributes, 'adib_10_travel-itinerary-cards');
    $html = '<section class="adib_10_travel_itinerary_cards-component"><h2>Travel Itinerary Cards</h2><dl>';
    if ($attributes['place'] !== '') { $html .= '<dt>Place</dt><dd>' . esc_html($attributes['place']) . '</dd>'; }
    if ($attributes['day'] !== '') { $html .= '<dt>Day</dt><dd>' . esc_html($attributes['day']) . '</dd>'; }
    if ($attributes['activity'] !== '') { $html .= '<dt>Activity</dt><dd>' . esc_html($attributes['activity']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_10_travel-itinerary-cards', 'adib_10_travel_itinerary_cards_render');

function adib_10_travel_itinerary_cards_assets() {
    $css = '.adib_10_travel_itinerary_cards-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_10_travel_itinerary_cards-component label{display:block;margin:.8rem 0}'
         . '.adib_10_travel_itinerary_cards-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_10_travel_itinerary_cards-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_10_travel_itinerary_cards-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_10_travel_itinerary_cards', false, [], '1.0.0');
    wp_enqueue_style('adib_10_travel_itinerary_cards');
    wp_add_inline_style('adib_10_travel_itinerary_cards', $css);
}
add_action('wp_enqueue_scripts', 'adib_10_travel_itinerary_cards_assets');

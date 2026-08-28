<?php
/**
 * Plugin Name: News Magazine Grid
 * Description: Creates a responsive news-magazine article grid.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_04_news_magazine_grid_render($attributes = []) {
    $attributes = shortcode_atts([
        'headline' => '',
        'category' => '',
        'summary' => ''
    ], $attributes, 'adib_04_news-magazine-grid');
    $html = '<section class="adib_04_news_magazine_grid-component"><h2>News Magazine Grid</h2><dl>';
    if ($attributes['headline'] !== '') { $html .= '<dt>Headline</dt><dd>' . esc_html($attributes['headline']) . '</dd>'; }
    if ($attributes['category'] !== '') { $html .= '<dt>Category</dt><dd>' . esc_html($attributes['category']) . '</dd>'; }
    if ($attributes['summary'] !== '') { $html .= '<dt>Summary</dt><dd>' . esc_html($attributes['summary']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_04_news-magazine-grid', 'adib_04_news_magazine_grid_render');

function adib_04_news_magazine_grid_assets() {
    $css = '.adib_04_news_magazine_grid-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_04_news_magazine_grid-component label{display:block;margin:.8rem 0}'
         . '.adib_04_news_magazine_grid-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_04_news_magazine_grid-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_04_news_magazine_grid-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_04_news_magazine_grid', false, [], '1.0.0');
    wp_enqueue_style('adib_04_news_magazine_grid');
    wp_add_inline_style('adib_04_news_magazine_grid', $css);
}
add_action('wp_enqueue_scripts', 'adib_04_news_magazine_grid_assets');

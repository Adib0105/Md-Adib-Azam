<?php
/**
 * Plugin Name: SEO Content Index
 * Description: Builds an alphabetized SEO content index.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_25_seo_content_index_render($attributes = []) {
    $attributes = shortcode_atts([
        'title' => '',
        'keyword' => '',
        'content_url' => ''
    ], $attributes, 'adib_25_seo-content-index');
    $html = '<section class="adib_25_seo_content_index-component"><h2>SEO Content Index</h2><dl>';
    if ($attributes['title'] !== '') { $html .= '<dt>Title</dt><dd>' . esc_html($attributes['title']) . '</dd>'; }
    if ($attributes['keyword'] !== '') { $html .= '<dt>Keyword</dt><dd>' . esc_html($attributes['keyword']) . '</dd>'; }
    if ($attributes['content_url'] !== '') { $html .= '<dt>Content Url</dt><dd>' . esc_html($attributes['content_url']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_25_seo-content-index', 'adib_25_seo_content_index_render');

function adib_25_seo_content_index_assets() {
    $css = '.adib_25_seo_content_index-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_25_seo_content_index-component label{display:block;margin:.8rem 0}'
         . '.adib_25_seo_content_index-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_25_seo_content_index-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_25_seo_content_index-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_25_seo_content_index', false, [], '1.0.0');
    wp_enqueue_style('adib_25_seo_content_index');
    wp_add_inline_style('adib_25_seo_content_index', $css);
}
add_action('wp_enqueue_scripts', 'adib_25_seo_content_index_assets');

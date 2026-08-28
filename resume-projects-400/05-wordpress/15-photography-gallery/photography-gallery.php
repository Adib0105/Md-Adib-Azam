<?php
/**
 * Plugin Name: Photography Gallery
 * Description: Renders an accessible photography gallery.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_15_photography_gallery_render($attributes = []) {
    $attributes = shortcode_atts([
        'image_url' => '',
        'alt_text' => '',
        'caption' => ''
    ], $attributes, 'adib_15_photography-gallery');
    $html = '<section class="adib_15_photography_gallery-component"><h2>Photography Gallery</h2><dl>';
    if ($attributes['image_url'] !== '') { $html .= '<dt>Image Url</dt><dd>' . esc_html($attributes['image_url']) . '</dd>'; }
    if ($attributes['alt_text'] !== '') { $html .= '<dt>Alt Text</dt><dd>' . esc_html($attributes['alt_text']) . '</dd>'; }
    if ($attributes['caption'] !== '') { $html .= '<dt>Caption</dt><dd>' . esc_html($attributes['caption']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_15_photography-gallery', 'adib_15_photography_gallery_render');

function adib_15_photography_gallery_assets() {
    $css = '.adib_15_photography_gallery-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_15_photography_gallery-component label{display:block;margin:.8rem 0}'
         . '.adib_15_photography_gallery-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_15_photography_gallery-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_15_photography_gallery-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_15_photography_gallery', false, [], '1.0.0');
    wp_enqueue_style('adib_15_photography_gallery');
    wp_add_inline_style('adib_15_photography_gallery', $css);
}
add_action('wp_enqueue_scripts', 'adib_15_photography_gallery_assets');

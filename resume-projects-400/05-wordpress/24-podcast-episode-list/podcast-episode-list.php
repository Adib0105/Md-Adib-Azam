<?php
/**
 * Plugin Name: Podcast Episode List
 * Description: Creates semantic podcast episode entries.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_24_podcast_episode_list_render($attributes = []) {
    $attributes = shortcode_atts([
        'episode' => '',
        'duration' => '',
        'audio_url' => ''
    ], $attributes, 'adib_24_podcast-episode-list');
    $html = '<section class="adib_24_podcast_episode_list-component"><h2>Podcast Episode List</h2><dl>';
    if ($attributes['episode'] !== '') { $html .= '<dt>Episode</dt><dd>' . esc_html($attributes['episode']) . '</dd>'; }
    if ($attributes['duration'] !== '') { $html .= '<dt>Duration</dt><dd>' . esc_html($attributes['duration']) . '</dd>'; }
    if ($attributes['audio_url'] !== '') { $html .= '<dt>Audio Url</dt><dd>' . esc_html($attributes['audio_url']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_24_podcast-episode-list', 'adib_24_podcast_episode_list_render');

function adib_24_podcast_episode_list_assets() {
    $css = '.adib_24_podcast_episode_list-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_24_podcast_episode_list-component label{display:block;margin:.8rem 0}'
         . '.adib_24_podcast_episode_list-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_24_podcast_episode_list-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_24_podcast_episode_list-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_24_podcast_episode_list', false, [], '1.0.0');
    wp_enqueue_style('adib_24_podcast_episode_list');
    wp_add_inline_style('adib_24_podcast_episode_list', $css);
}
add_action('wp_enqueue_scripts', 'adib_24_podcast_episode_list_assets');

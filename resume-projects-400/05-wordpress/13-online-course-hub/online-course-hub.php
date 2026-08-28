<?php
/**
 * Plugin Name: Online Course Hub
 * Description: Builds an online-course directory.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_13_online_course_hub_render($attributes = []) {
    $attributes = shortcode_atts([
        'course' => '',
        'instructor' => '',
        'lessons' => ''
    ], $attributes, 'adib_13_online-course-hub');
    $html = '<section class="adib_13_online_course_hub-component"><h2>Online Course Hub</h2><dl>';
    if ($attributes['course'] !== '') { $html .= '<dt>Course</dt><dd>' . esc_html($attributes['course']) . '</dd>'; }
    if ($attributes['instructor'] !== '') { $html .= '<dt>Instructor</dt><dd>' . esc_html($attributes['instructor']) . '</dd>'; }
    if ($attributes['lessons'] !== '') { $html .= '<dt>Lessons</dt><dd>' . esc_html($attributes['lessons']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_13_online-course-hub', 'adib_13_online_course_hub_render');

function adib_13_online_course_hub_assets() {
    $css = '.adib_13_online_course_hub-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_13_online_course_hub-component label{display:block;margin:.8rem 0}'
         . '.adib_13_online_course_hub-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_13_online_course_hub-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_13_online_course_hub-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_13_online_course_hub', false, [], '1.0.0');
    wp_enqueue_style('adib_13_online_course_hub');
    wp_add_inline_style('adib_13_online_course_hub', $css);
}
add_action('wp_enqueue_scripts', 'adib_13_online_course_hub_assets');

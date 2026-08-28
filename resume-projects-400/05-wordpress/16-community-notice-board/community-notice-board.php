<?php
/**
 * Plugin Name: Community Notice Board
 * Description: Accepts a sanitized community notice for moderator review.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_16_community_notice_board_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_16_community_notice_board_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_16_community_notice_board_nonce'])), 'adib_16_community_notice_board_submit')) {
        $values['author'] = isset($_POST['adib_16_community_notice_board_author']) ? sanitize_text_field(wp_unslash($_POST['adib_16_community_notice_board_author'])) : '';
        $values['email'] = isset($_POST['adib_16_community_notice_board_email']) ? sanitize_email(wp_unslash($_POST['adib_16_community_notice_board_email'])) : '';
        $values['notice'] = isset($_POST['adib_16_community_notice_board_notice']) ? sanitize_text_field(wp_unslash($_POST['adib_16_community_notice_board_notice'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_16_community_notice_board-component"><h2>Community Notice Board</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_16_community_notice_board_submit', 'adib_16_community_notice_board_nonce', true, false);
    $html .= '<label>Author<input name="adib_16_community_notice_board_author" type="text" required></label>';
    $html .= '<label>Email<input name="adib_16_community_notice_board_email" type="email" required></label>';
    $html .= '<label>Notice<input name="adib_16_community_notice_board_notice" type="text" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_16_community-notice-board', 'adib_16_community_notice_board_render');

function adib_16_community_notice_board_assets() {
    $css = '.adib_16_community_notice_board-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_16_community_notice_board-component label{display:block;margin:.8rem 0}'
         . '.adib_16_community_notice_board-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_16_community_notice_board-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_16_community_notice_board-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_16_community_notice_board', false, [], '1.0.0');
    wp_enqueue_style('adib_16_community_notice_board');
    wp_add_inline_style('adib_16_community_notice_board', $css);
}
add_action('wp_enqueue_scripts', 'adib_16_community_notice_board_assets');


	<div id="footer">
		<span id="copyright">&copy; <?php echo( date('Y') ); ?> <?php barthelme_admin_hCard(); ?></span>
		<span class="meta-sep">|</span>
		<span id="generator-link"><?php _e('Thanks, <a href="http://wordpress.org/" title="WordPress" rel="generator">WordPress</a>', 'barthelme') ?></span>
		<span class="meta-sep">|</span>
		<span id="theme-link"><a href="http://www.plaintxt.org/themes/barthelme/" title="<?php _e('Barthelme theme for WordPress', 'barthelme') ?>" rel="follow designer">Barthelme</a> <?php _e('theme by', 'barthelme') ?> <span class="vcard"><a class="url fn n"  title="plaintxt.org" rel="follow designer">PlainTXT.org</a></span></span><!-- Theme design credit, that's all -->
		<span class="meta-sep">|</span>
		<span id="web-standards"> <?php _e('Standards Compliant', 'barthelme') ?> <a href="http://validator.w3.org/check/referer" title="Valid XHTML">XHTML</a> &amp; <a href="http://jigsaw.w3.org/css-validator/validator?profile=css2&amp;warning=2&amp;uri=<?php bloginfo('stylesheet_url'); ?>" title="<?php _e('Valid CSS', 'barthelme') ?>">CSS</a></span>
		<span class="meta-sep">|</span>
		<span id="footer-rss"> <?php _e('RSS', 'barthelme') ?> <a href="<?php bloginfo('rss2_url') ?>" title="<?php echo _wp_specialchars(get_bloginfo('name'), 1) ?> <?php _e('RSS 2.0 Feed', 'barthelme') ?>" rel="alternate" type="application/rss+xml"><?php _e('Posts', 'barthelme') ?></a> &amp; <a href="<?php bloginfo('comments_rss2_url') ?>" title="<?php echo _wp_specialchars(bloginfo('name'), 1) ?> Comments RSS 2.0 Feed" rel="alternate" type="application/rss+xml"><?php _e('Comments', 'barthelme') ?></a></span>
	</div><!-- #footer -->

<?php wp_footer() // Do not remove; helps plugins work ?>

</div><!-- #wrapper -->

</body><!-- end trasmission -->
</html>
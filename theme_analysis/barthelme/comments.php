<?php
	if ( 'comments.php' == basename($_SERVER['SCRIPT_FILENAME']) )
		die ( 'Please do not load this page directly. Thanks!' );
?>
<div class="comments">
<?php
	$req = get_option('require_name_email'); // Checks if fields are required. Thanks, Adam. ;-)
	if ( !empty($post->post_password) ) :
		if ( $_COOKIE['wp-postpass_' . COOKIEHASH] != $post->post_password ) :
?>
				<div class="protected"><?php _e('This post is protected. Enter the password to view any comments.', 'barthelme') ?></div>
			</div><!-- .comments -->
<?php
		return;
	endif;
endif;
?>
<?php if ( $comments ) : ?>
<?php global $barthelme_comment_alt // Gives .alt class for every-other comment/pingback ?>
<?php
$ping_count = $comment_count = 0;
foreach ( $comments as $comment )
	get_comment_type() == "comment" ? ++$comment_count : ++$ping_count;
?>
<?php if ( $comment_count ) : ?>
<?php $barthelme_comment_alt = 0 // Resets comment count for .alt classes ?>

	<h3 class="comment-header" id="numcomments"><?php printf(__($comment_count > 1 ? '<span class="comment-count"><span class="meta-sep">{</span> %d <span class="meta-sep">}</span></span> Comments' : '<span class="comment-count"><span class="meta-sep">{</span> 1 <span class="meta-sep">}</span></span> Comments'), $comment_count) ?></h3>
	<ol id="comments" class="commentlist">
<?php foreach ($comments as $comment) : ?>
<?php if ( get_comment_type() == "comment" ) : ?>
		<li id="comment-<?php comment_ID() ?>" class="<?php barthelme_comment_class() ?>">
			<div class="comment-meta">
				<span class="comment-author vcard"><?php barthelme_commenter_link() ?></span>
				<span class="meta-sep">|</span>
				<span class="comment-datetime"><?php printf(__('<abbr class="comment-published" title="%1$s">%2$s at %3$s</abbr></span>', 'barthelme'),
						get_the_time('Y-m-d\TH:i:sO'),
						get_comment_date(),
						get_comment_time() ); ?>

				<span class="meta-sep">|</span>
				<span class="comment-permalink"><a href="#comment-<?php comment_ID() ?>" title="Permalink to this comment"><?php _e('Permalink', 'barthelme') ?></a></span>
<?php edit_comment_link(__('Edit', 'barthelme'), "\t\t\t\t<span class=\"meta-sep\">|</span>\n\t\t\t\t<span class=\"comment-edit\">", "</span>\n"); ?>
			</div>
			<?php if ($comment->comment_approved == '0') : ?><span class="unapproved"><?php _e('Your comment is awaiting moderation.', 'barthelme') ?></span><?php endif; ?>

			<?php comment_text() ?>
		</li>

<?php endif; ?>
<?php endforeach; ?>

	</ol><!-- end #comments .commentlist -->

<?php endif; ?>

<?php if ( $ping_count ) : ?>
<?php $barthelme_comment_alt = 0 // Resets comment count for .alt classes for pingbacks ?>

	<h3 class="comment-header" id="numpingbacks"><?php printf(__($ping_count > 1 ? '<span class="comment-count"><span class="meta-sep">{</span> %d <span class="meta-sep">}</span></span> Trackbacks' : '<span class="comment-count"><span class="meta-sep">{</span> 1 <span class="meta-sep">}</span></span> Trackback', 'barthelme'), $ping_count) ?></h3>
	<ol id="pingbacks" class="commentlist">
<?php foreach ( $comments as $comment ) : ?>
<?php if ( get_comment_type() != "comment" ) : ?>
		<li id="comment-<?php comment_ID() ?>" class="<?php barthelme_comment_class() ?>">
			<div class="comment-meta">
				<span class="pingback-author vcard"><span class="fn n url org"><?php comment_author_link() ?></span></span>
				<span class="meta-sep">|</span>
				<span class="pingback-datetime"><?php printf(__('<abbr class="comment-published" title="%1$s">%2$s at %3$s</abbr></span>', 'barthelme'),
						get_the_time('Y-m-d\TH:i:sO'),
						get_comment_date(),
						get_comment_time() ); ?>

				<span class="meta-sep">|</span>
				<span class="comment-permalink"><a href="#comment-<?php comment_ID() ?>" title="Permalink to this comment">Permalink</a></span>
<?php edit_comment_link(__('Edit', 'barthelme'), "\t\t\t\t<span class=\"meta-sep\">|</span>\n\t\t\t\t<span class=\"comment-edit\">", "</span>\n"); ?>
			</div>
			<?php if ($comment->comment_approved == '0') : ?><span class="unapproved"><?php _e('Your comment is awaiting moderation.', 'barthelme') ?></span><?php endif; ?>
			<?php comment_text() ?>
		</li>

<?php endif ?>
<?php endforeach; ?>

	</ol><!-- #pingbacks .commentlist -->

<?php endif ?>
<?php endif ?>

<?php if ( 'open' == $post->comment_status ) : ?>

	<h3 id="respond"><?php _e('Post a Comment', 'barthelme') ?></h3>
<?php if ( get_option('comment_registration') && !$user_ID ) : ?>
	<div id="mustlogin"><?php printf(__('You must be <a href="%s" title="Log in">logged in</a> to post a comment.', 'barthelme'),
			get_option('siteurl') . '/wp-login.php?redirect_to=' . get_permalink() ) ?></div>

<?php else : ?>

	<div class="formcontainer">	

		<form id="commentform" action="<?php echo get_option('siteurl'); ?>/wp-comments-post.php" method="post">
<?php if ( $user_ID ) : ?>

			<div id="loggedin"><?php printf(__('Logged in as <a href="%1$s" title="View your profile" class="fn">%2$s</a>. <a href="%3$s" title="Log out of this account">Log out?</a>', 'barthelme'),
					get_option('siteurl') . '/wp-admin/profile.php',
					_wp_specialchars($user_identity, true),
					get_option('siteurl') . '/wp-login.php?action=logout&amp;redirect_to=' . get_permalink() ) ?></div>

<?php else : ?>

			<div id="comment-notes"><?php _e('Your email is <em>never</em> published nor shared.', 'barthelme') ?> <?php if ($req) _e('Required fields are marked <span class="req-field">*</span>', 'barthelme') ?></div>

			<div class="form-label"><label for="author"><?php _e('Name', 'barthelme') ?><?php if ($req) _e(' <span class="req-field">*</span>', 'barthelme') ?></label></div>
			<div class="form-input"><input id="author" name="author" type="text" value="<?php echo $comment_author ?>" size="30" maxlength="20" tabindex="3" /></div>

			<div class="form-label"><label for="email"><?php _e('Email', 'barthelme') ?><?php if ($req) _e(' <span class="req-field">*</span>', 'barthelme') ?></label></div>
			<div class="form-input"><input id="email" name="email" type="text" value="<?php echo $comment_author_email ?>" size="30" maxlength="50" tabindex="4" /></div>

			<div class="form-label"><label for="url"><?php _e('Website', 'barthelme') ?></label></div>
			<div class="form-input"><input id="url" name="url" type="text" value="<?php echo $comment_author_url ?>" size="30" maxlength="50" tabindex="5" /></div>

<?php endif ?>

			<div class="form-label"><label for="comment"><?php _e('Comment', 'barthelme') ?></label></div>
			<div class="form-textarea"><textarea id="comment" name="comment" cols="45" rows="8" tabindex="6"></textarea></div>
			<div class="form-submit"><input id="submit" name="submit" type="submit" value="<?php _e('Submit comment', 'barthelme') ?>" tabindex="7" /><input type="hidden" name="comment_post_ID" value="<?php echo $id; ?>" /></div>

<?php do_action('comment_form', $post->ID); ?>
		</form><!-- #commentform -->
	</div><!-- .formcontainer -->

<?php endif ?>
<?php endif ?>
</div><!-- .comments -->

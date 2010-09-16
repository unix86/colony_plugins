<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="/template_error_handler/css/main.css" />
        <script type="text/javascript" src="/template_error_handler/js/main.js"></script>
    </head>
    <body>
        <div id="wiki-header">
            <div class="wiki-header-contents">
                <div class="logo-image">
                    <img src="/template_error_handler/images/colony_logo.png"/>
                </div>
            </div>
        </div>
        <div id="wiki-contents">
            <p></p>
            <div class="highlight">
                <img class="error-image" src="/template_error_handler/images/${out_none value=error_image xml_escape=True /}.png"/>
                <div class="error-text" tyle="float: left; margin-left: 18px;">
                    <b>There was a problem in colony web server...</b>
                    <p>Error ${out_none value=error_code xml_escape=True /} - ${out_none value=error_description xml_escape=True /}</p>
                </div>
            </div>
            <p></p>
			<div class="directory-listing">		
					<div class="table-view">
						<table cellspacing="0">
							<thead>
								<tr>
									<th class="column name">Name</th>
									<th class="column date">Last Modified</th>
									<th class="column size">Size</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td class="name folder-small"><a href="#">Folder</a></td>
									<td class="date">31 Dec 2009</td>
									<td class="size">18K</td>
								</tr>
								<tr>
									<td class="name folder-small"><a href="#">Folder</a></td>
									<td class="date">31 Dec 2009</td>
									<td class="size">18K</td>
								</tr>
								<tr>
									<td class="name folder-small"><a href="#">Folder</a></td>
									<td class="date">31 Dec 2009</td>
									<td class="size">18K</td>
								</tr>
								<tr>
									<td class="name folder-small"><a href="#">Folder</a></td>
									<td class="date">31 Dec 2009</td>
									<td class="size">18K</td>
								</tr>
								<tr>
									<td class="name folder-small"><a href="#">Folder</a></td>
									<td class="date">31 Dec 2009</td>
									<td class="size">18K</td>
								</tr>
								<tr>
									<td class="name file-small"><a href="#">text-file.txt</a></td>
									<td class="date">05 Oct 2009</td>
									<td class="size">35K</td>
								</tr>
							</tbody>
							<tfoot></tfoot>
						</table>
					</div>
					<div class="view-modes">
						<a href="#" class="active">Table</a>
						<a href="#">Mosaic</a>
						<a href="#">Thumbnail</a>
					</div>
				</div>
        </div>
        <div id="wiki-footer">
            <div class="wiki-footer-contents">
                <div class="logo-image">
                    <a href="http://getcolony.com">
                        <img src="/template_error_handler/images/powered_by_colony.png"/>
                    </a>
                </div>
                <div class="separator">
                    <img src="/template_error_handler/images/separator.png"/>
                </div>
                <div class="text-contents">Document provided by colony framework in ${out_none value=delta_time xml_escape=True /} seconds
                    <br/>Copyright
                    <a href="http://www.hive.pt">Hive Solutions Lda.</a> distributed under
                    <a href="http://creativecommons.org/licenses/by-sa/3.0"> Creative Commons License</a>
                </div>
            </div>
        </div>
    </body>
</html>

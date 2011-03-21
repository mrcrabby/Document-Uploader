$(function(){
	$('#firstlog').dialog({
					autoOpen: true,
					width: 650,
					buttons: {
						"Ok": function() { 
							$(this).dialog("close"); 
						} 

					}
				});

				
				// Dialog			
				$('#dialog').dialog({
					autoOpen: false,
					width: 600,
					buttons: {
						"Ok": function() { 
							$(this).dialog("close"); 
						} 
					}
				});
				
				// Dialog Link
				$('#dialog_link').click(function(){
					$('#dialog').dialog('open');
					return false;
				});
				$('#file_upload').fileUploadUI({
			        uploadTable: $('#files'),
			        downloadTable: $('#files'),
			        buildUploadRow: function (files, index) {
			            return $('<tr><td>' + files[index].name + '<\/td>' +
			                    '<td class="file_upload_progress"><div><\/div><\/td>' +
			                    '<td class="file_upload_cancel">' +
			                    '<button class="ui-state-default ui-corner-all" title="Cancel">' +
			                    '<span class="ui-icon ui-icon-cancel">Cancel<\/span>' +
			                    '<\/button><\/td><\/tr>');
			        },
			        buildDownloadRow: function (file) {
			            return $('<tr><td>' + file.name + '<\/td><\/tr>');
			        }
			    });			
			
			
});

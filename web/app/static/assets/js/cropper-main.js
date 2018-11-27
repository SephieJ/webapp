
      var Cropper = window.Cropper;
      var URL = window.URL || window.webkitURL;
      var container = document.querySelector('.img-container');
      var image = container.getElementsByTagName('img').item(0);
      var actions = document.getElementById('btn-container-list');
      var options = {
            aspectRatio: 1 / 1,
            autoCropArea: 1,
            dragMode: 'crop',
            setData: {width: 480, height: 270}
          };
      var cropper = new Cropper(image, options);
      var originalImageURL = image.src;
      var uploadedImageURL;
      var pic_wrap = "";
      var pic_id = "";
      var pic_input = "";
      var original_image = {};
      var token = $('input[name=csrf_token]').val();
      var image_full = "";
      var image_cropped = "";
      var image_json = "";
      var upload_img_ctr = 0;
      var is_recropped = false;
      var data_img_full = null;


      window.onload = function () {

      'use strict';


      // Buttons
      if (!document.createElement('canvas').getContext) {
        $('button[data-method="getCroppedCanvas"]').prop('disabled', true);
      }

      if (typeof document.createElement('cropper').style.transition === 'undefined') {
        $('button[data-method="rotate"]').prop('disabled', true);
        $('button[data-method="scale"]').prop('disabled', true);
      }

      // Methods
      actions.querySelector('.docs-buttons').onclick = function (event) {
        var e = event || window.event;
        var target = e.target || e.srcElement;
        var result;
        var input;
        var data;

        if (!cropper) {
          return;
        }

        while (target !== this) {
          if (target.getAttribute('data-method')) {
            break;
          }

          target = target.parentNode;
        }

        if (target === this || target.disabled || target.className.indexOf('disabled') > -1) {
          return;
        }

        data = {
          method: target.getAttribute('data-method'),
          target: target.getAttribute('data-target'),
          option: target.getAttribute('data-option'),
          secondOption: target.getAttribute('data-second-option')
        };

        if (data.method) {
          if (typeof data.target !== 'undefined') {
            input = document.querySelector(data.target);

            if (!target.hasAttribute('data-option') && data.target && input) {
              try {
                data.option = JSON.parse(input.value);
              } catch (e) {
                console.log(e.message);
              }
            }
          }

          if (data.method === 'getCroppedCanvas') {
            data.option = JSON.parse(data.option);
          }


          result = cropper[data.method](data.option, data.secondOption);

          switch (data.method) {
            case 'scaleX':
            case 'scaleY':
              target.setAttribute('data-option', -data.option);
              break;

            case 'getCroppedCanvas':
              if (result) {
                var inputTypeHidden = "";

                if(is_recropped == true){
                    if (document.getElementById(pic_id + "-temp").value == ""){
                        image_full = null;
                    } else {
                        image_full = document.getElementById(pic_id + "-temp").value;
                    }
                } else {
                    image_full = document.getElementById(pic_id + "-temp").value;
                }

                image_cropped = result.toDataURL('image/png');

                image_json = {
                    "image": image_cropped,
                    "image_full": image_full,
                    "pic_id": pic_id,
                    "pic_wrap": pic_wrap
                };

                //Spinner class
                document.getElementById(pic_id).style.display="none";
                $('#' + pic_wrap).find('i').removeClass('fa fa-picture-o');
                $('#' + pic_wrap).find('i').addClass('fa fa-circle-o-notch fa-spin fa-2x fa-fw');
                $('#' + pic_wrap).find('i').css('display','block');
                $('#' + pic_wrap).find('.thumb-del').remove();

                upload_img_ctr += 1;

                //AJAX call for uploading upon image cropping
                $.ajax({
                    headers: {'X-CSRF-TOKEN' : token},
                    type: 'POST',
                    dataType : 'json',
                    data: JSON.stringify(image_json),
                    contentType: 'application/json; charset=utf-8',
                    url: '/resources/upload/images',
                    success: function(data){
                        $('#' + pic_id + 'kk').remove();

                        if(is_recropped == true){
                            if(document.getElementById(pic_id + "-temp").value == ""){
                                data_img_full = document.getElementById(pic_id + "-temp-url").value;
                            } else {
                                data_img_full = data['image_url_full'];
                            }
                        } else {
                            data_img_full = data['image_url_full'];
                        }

                        inputTypeHidden = '<input class="inputImage_url" type="hidden" id="' + data['pic_id'] + 'kk" value="' + data['image_url'] + "," + data_img_full + '" name="inputImage_url[]">';

                        if(data['pic_id'] == "inputImage1-pic"){
                            $('.photosfield').prepend(inputTypeHidden);
                        } else {
                            $('.photosfield').append(inputTypeHidden);
                        }

                        //Render image if upload is successful
                        $('#' + data['pic_wrap']).find('i').hide();
                        document.getElementById(data['pic_id']).src = result.toDataURL('image/png');
                        document.getElementById(data['pic_id']).style.display="block";
                        document.getElementById('btn-container-list').style.display="none";

                        $('#' + data['pic_wrap']).find('button').remove();
                        $('#' + data['pic_wrap']).append('<button class="btn btn-sm btn-danger thumb-del" type="button" id="remove-button"><i class="fa fa-times fa-lg" aria-hidden="true" id="remove-button"></i></button>');

                        upload_img_ctr -= 1;
                        is_recropped = false;

                    },
                    error: function(msg){
                      console.log(msg);
                      $('#' + pic_wrap).find('i').removeClass('fa fa-circle-o-notch fa-spin fa-2x fa-fw');
                      $('#' + pic_wrap).find('i').addClass('fa fa-picture-o');
                    }
                });

                image_full = "";
                image_cropped = "";
                image_json = "";
                image.src = "";
                data_img_full = null;
                cropper.destroy();
              }

              break;

            case 'destroy':
              cropper = null;

              if (uploadedImageURL) {
                URL.revokeObjectURL(uploadedImageURL);
                uploadedImageURL = '';
                image.src = originalImageURL;
              }

              break;
          }

          if (typeof result === 'object' && result !== cropper && input) {
            try {
              input.value = JSON.stringify(result);
            } catch (e) {
              console.log(e.message);
            }
          }
        }
      };

      document.body.onkeydown = function (event) {
        var e = event || window.event;

        if (!cropper || this.scrollTop > 300) {
          return;
        }

        switch (e.keyCode) {
          case 37:
            e.preventDefault();
            cropper.move(-1, 0);
            break;

          case 38:
            e.preventDefault();
            cropper.move(0, -1);
            break;

          case 39:
            e.preventDefault();
            cropper.move(1, 0);
            break;

          case 40:
            e.preventDefault();
            cropper.move(0, 1);
            break;
        }
      };


      // Import image

      if (URL) {
        $('.inputImage').on('change',function(){
          var inputImage = this;
          pic_id = this.id + '-pic';
          pic_wrap = this.id + '-wrap';
          pic_input = this.id + '-input';
          import_image(inputImage);
        });

      } else {
        inputImage.disabled = true;
        inputImage.parentNode.className += ' disabled';
      }



      $('.rs-thumb-content').on('click', function(e) {
          var thumb_img = $(this).find('img');
          var str = this.id;
          var res = str.replace("-wrap","");
          var target_id = e.target.id;

          if (target_id == 'remove-button') {
            pic_id = res + '-pic';
            cropper.destroy();
            document.getElementById('img-cropper-container').style.display="none";
            document.getElementById(pic_id).src = '';
            document.getElementById(pic_id + "-temp").value = '';
            document.getElementById(pic_id + "kk").value = '';
            $('#' + str).find('i').removeClass('fa fa-circle-o-notch fa-spin fa-2x fa-fw');
            $('#' + str).find('i').addClass('fa fa-picture-o');
            $('#' + str).find('i').css('display','block');
            $('#' + pic_id).hide();
            $(this).find('button').remove()
          } else {
            if ($(thumb_img).attr('src') == '') {
              $('#' + res).trigger('click');

            } else {

              pic_id = res + '-pic';
              pic_wrap = str;
              image.src = $(thumb_img).attr('src');
              is_recropped = true;
              cropper.destroy();
              cropper = new Cropper(image, options);
              document.getElementById('img-cropper-container').style.display="block";

            }
            document.getElementById('btn-container-list').style.display="block";
          }
          e.preventDefault();
      });

    };

    function import_image(source_id) {

          var files = source_id.files;
          var file;

          if (cropper && files && files.length) {
            file = files[0];

            var file_types = ['png','jpg','jpeg'];
            var file_type_ctr = 0;

            if (files && files.length) {
                file = files[0];

                for(var type in file_types){
                    if(file_types[type] === file.type.replace("image/","")){
                        file_type_ctr += 1;
                    }
                }

                if(file_type_ctr == 0){
                    window.alert('Invalid file format.');
                    return;
                }
            }


            if (/^image\/\w+/.test(file.type)) {
              if (uploadedImageURL) {
                URL.revokeObjectURL(uploadedImageURL);
              }

              image.src = uploadedImageURL = URL.createObjectURL(file);

              //to convert file to base64
              var reader = new window.FileReader();
              reader.onloadend = function() {
                    var base64data = reader.result;
                    original_image[source_id.id] = base64data;
                    $('#' + source_id.id + '-pic-temp').remove();
                    var inputTypeHidden = '<input type="hidden" id="' + source_id.id + '-pic-temp" value="' + base64data + '" name="temp_full">';
                    $('.temporary-full-image').append(inputTypeHidden);
              }
              reader.readAsDataURL(file);




              cropper.destroy();
              cropper = new Cropper(image, options);
              source_id.value = null;

              document.getElementById('img-cropper-container').style.display="block";
              document.getElementById('btn-container-list').style.display="block";

            } else {
              window.alert('Please choose an image file.');
            }
          }

    }

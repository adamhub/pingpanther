<div class="form">
    %if site:
    <div class="hidden">
        <input class="form_id" type="hidden" name="id" value="{{site['id']}}"/>
    </div>
    %end
    <div class="form_left">
      <div class="div_addsite" >
        <div class="form_field">
            Site<br/>
            %if site:
                <input class="form_url" value="{{site['url']}}" name="url" type="text" />
            %else:
                <input class="form_url" value="" name="url" type="text" />
            %end
        </div>
        <div class="form_field">
            Tags<br/>
            %if site:
                %tag_string = ""
                %for i, tag in enumerate(site['tags']):
                    %if i == len(site['tags']) - 1:
                        %tag_string += tag
                    %else:
                        %tag_string += tag + ", "
                    %end
                %end
                <textarea class="form_tags" name="tags" >{{tag_string}}</textarea>
            %else:
                <textarea class="form_tags" name="tags" ></textarea>
            %end
            <p class="help_text">
                separate with comma
            </p>
        </div>
      </div>
      
    </div>

    <div class="form_right">
        <div class="form_field">
            Check Frequency (mins)
            <input class="input-small form_frequency"
                name="frequency"
                type="text"
                %if site:
                    value={{site['frequency']}}
                %else:
                    value=5
                %end
            />
        </div>
        <div class="form_field">
            How many fails trigger alert?
            <input class="input-small form_fail_trigger"
                name="fail_trigger"
                type="text"
                %if site:
                    value={{site['fail_trigger']}}
                %else:
                    value=1
                %end
            />
        </div>
        <div class="form_field">
            Allowed seconds to respond
            <input class="input-small form_respond_seconds"
                name="respond_seconds"
                type="text"
                %if site:
                    value={{site['respond_seconds']}}
                %else:
                    value=10
                %end
            />
        </div>
    </div>
    <div class="clearfix"></div>
    <div class="form_buttons">
        %if site:
            %if authenticated:
            <a class="editsite_save_btn btn" data-id="{{ site['id'] }}" data-url="{{ site['url'] }}" href="javascript:;" >
                save
            </a><br/>
            %end
            <a class="editsite_cancel_btn btn" href="#" >cancel</a>
        %else:
            %if authenticated:
            <a id="addsite_add_btn" href="javascript:;" class="btn">
                add
            </a><br/>
            %end
            <a id="addsite_cancel_btn" href="javascript:;" class="btn">cancel</a>
        %end
    </div>
  </div>

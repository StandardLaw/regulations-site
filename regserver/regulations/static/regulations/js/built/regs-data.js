define("regs-data",["jquery","underscore","backbone","./regs-helpers","./regs-dispatch"],function(e,t,n,r,i){n.RegModel=n.Model.extend({regStructure:[],content:{},parse:function(e){if(typeof e=="object")for(var t in e)e.hasOwnProperty(t)&&(t==="label"&&this.set(e[t].text,e.text),r.isIterable(e[t])&&this.parse(e[t]));return this},set:function(e,n){var r=this.has(e),i;return r?i=r:(this.content[e]=n,i=n,t.indexOf(this.regStructure,e)===-1&&this.regStructure.push(e)),i},has:function(e){return this.content[e]?this.content[e]:!1},get:function(e){var t=this.has(e)||this.request(e);return t},fetch:function(e){return this.get(e)},request:function(t){var n=this.getAJAXUrl(t),r;return r=e.ajax({url:n,success:function(e){this.set(t,e)}.bind(this)}),r},getAJAXUrl:function(e){var t,n=i.getURLPrefix();return n?t="/"+n+"/partial/":t="/partial/",t+=e+"/"+i.getVersion(),t},getChildren:function(e){var t=[],n=this.regStructure.length,r=new RegExp(e+"[-,a-z,0-9]");while(n--)r.test(this.regStructure[n])&&t.push(this.regStructure[n]);return t},getParent:function(e){var t,n;return n=e.split("-"),n.pop(),t=n.join("-"),this.regStructure.indexOf(t)!==-1?this.content[t]:!1},sync:function(){return},save:function(){return},destroy:function(){return}});var s=new n.RegModel;return s});
var table = $('table');
    
$('#facility_header, #city_header')
    .wrapInner('<span title="sort this column"/>')
    .each(function(){
        
        var th = $(this),
            thIndex = th.index(),
            inverse = false;
        
        th.click(function(){
            
            table.find('td').filter(function(){
                
                return $(this).index() === thIndex;
                
            }).sortElements(function(a, b){
                
                return $.text([a]) > $.text([b]) ?
                    inverse ? -1 : 1
                    : inverse ? 1 : -1;
                
            }, function(){
                
                // parentNode is the element we want to move
                return this.parentNode; 
                
            });
            
            inverse = !inverse;
                
        });
            
    });

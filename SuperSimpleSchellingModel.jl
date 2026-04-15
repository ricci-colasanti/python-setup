using Plots

function init_grid()
    for row in 2:size-1
        for col in 2:size-1
            if rand()<0.9
                grid[row,col]=rand(1:2)
            end
        end
    end
end;

function count_neighbours(row,col)
    count =0
    neighbours =0
    for r in row-1:row+1
        for c in col-1:col+1
            if grid[r,c]>0
                count+=1
            end
            if grid[r,c]==grid[row,col]
                neighbours+=1
            end
        end
    end
    return count, neighbours
end;

function print_grid()
    for col in 2:size-1
        for row in 2:size-1
            count, neighbours = count_neighbours(row,col)
            print(grid[row,col])
        end     
        println()
    end 
end;


function move()
    for col in 2:size-1
        for row in 2:size-1
            count, neighbours = count_neighbours(row,col)
            if count>0
                if neighbours/count < 0.5
                    while true
                        r = rand(2:size-1)
                        c = rand(2:size-1)
                        if grid[r,c]==0
                            grid[r,c] = grid[row,col]
                            grid[row,col] =0
                            break
                        end
                    end
                end
            end
        end     
    end 
end;



function plot_grid()
    heatmap(grid,
            color = cgrad([:white, :red, :blue], [0, 1, 2]),
            clims = (0, 2),
            aspect_ratio = :equal,
            framestyle = :none,
            ticks = false,
            colorbar = false)  # Clean look for ABMs
end;



size = 20
grid = zeros(Int,size,size)
init_grid()
for i in 1:30
    move()
end
plot_grid()

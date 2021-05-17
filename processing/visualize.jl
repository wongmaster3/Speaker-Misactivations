using AbstractPlotting.GeometryBasics
using CSV
using GLMakie


function load_light_data(filename="light_logs/home_mini/common_uk/home_mini_common_uk_1_light_activations.csv")
    return [(floor(Int, row.start_time), ceil(Int, row.end_time)) for row in CSV.File(filename)]
end

function load_word_data(filename="light_logs/home_mini/common_uk/home_mini_common_uk_1_word_generations.csv")
    return [(row.word, floor(Int, row.start_time), ceil(Int, row.end_time)) for row in CSV.File(filename)]
end

function load_network_data(filename="wireshark_logs/home_mini/home_mini_common_uk_network.csv")
    return [(round(Int, row.time), row.size) for row in CSV.File(filename)]
end

function visualize(word_data, light_data, network_data, company="google";
        fig=current_figure(), x=1, y=1)

    trigger_word = company == "google" ? "ok_google" : "hey_alexa"
    first_time = first(word_data)[2]

    ax1 = fig[x, y] = Axis(fig)
    ax1.xlabel = "time since first word (s)"
    ax1.ylabel = "relative activations"

    scaled_network_data = map(network_data) do (time, size)
        return (time - first_time, size / 1500)
    end
    lines!(ax1, scaled_network_data, color=:black, label="network packets")

    x = Int[]; y = Int[]
    for (word, start_time, end_time) in word_data
        if word == trigger_word
            push!(x, start_time - first_time)
            push!(x, start_time - first_time)
            push!(y, 0)
            push!(y, -1)
        end
    end
    linesegments!(ax1, x, y, color=:blue, label="trigger word start")

    light_x = Int[]; light_y = Int[]
    for (start_time, end_time) in light_data
        push!(light_x, start_time - first_time)
        push!(light_y, -2)

        push!(light_x, start_time - first_time)
        push!(light_y, -1)

        push!(light_x, end_time - first_time)
        push!(light_y, -1)

        push!(light_x, end_time - first_time)
        push!(light_y, -2)
    end
    lines!(ax1, light_x, light_y, color=:red, label="light activation")

    fig, ax1
end

function visualize_data(word_filename, light_filename, network_filename, company="google";
        kwargs...)
    word_data = load_word_data(word_filename)
    light_data = load_light_data(light_filename)
    network_data = load_network_data(network_filename)

    visualize(word_data, light_data, network_data, company; kwargs...)
end

fig = Figure(backgroundcolor = RGBf0(0.98, 0.98, 0.98),
            resolution = (1000, 700))

_, ax1 = visualize_data(
    "experiments/echo_common_3.co.in/echo_co.in_3_word_generations.csv",
    "experiments/echo_common_3.co.in/echo_co.in_3_light_activations.csv",
    "experiments/echo_common_3.co.in/echo_co.in_3.csv", "amazon",
    fig=fig, x=1, y=1)
ax1.title = "Amazon Echo, Common Words with Indian Accent"
axislegend()

_, ax2 = visualize_data(
    "experiments/echo_common_3.co.uk/echo_co.uk_3_word_generations.csv",
    "experiments/echo_common_3.co.uk/echo_co.uk_3_light_activations.csv",
    "experiments/echo_common_3.co.uk/echo_co.uk_3.csv", "amazon",
    fig=fig, x=2, y=1)
ax2.title = "Amazon Echo, Common Words with UK Accent"

_, ax3 = visualize_data(
    "experiments/echo_common_3.com/echo_com_3_word_generations.csv",
    "experiments/echo_common_3.com/echo_com_3_light_activations.csv",
    "experiments/echo_common_3.com/echo_com_3.csv", "amazon",
    fig=fig, x=3, y=1)
ax3.title = "Amazon Echo, Common Words with US Accent"

linkaxes!(ax1, ax2, ax3)
hidexdecorations!(ax2, grid = false)
hidexdecorations!(ax1, grid = false)


fig
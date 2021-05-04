using CSV
using GLMakie


function load_light_data(filename="light_logs/home_mini/common_uk/home_mini_common_uk_1_light_activations.csv")
    data = Tuple{Float64, Float64}[]
    for row in CSV.File(filename)
        push!(data, (row.start_time, row.end_time))
    end
    return data
end

function load_word_data(filename="light_logs/home_mini/common_uk/home_mini_common_uk_1_word_generations.csv")
    data = Tuple{String, Float64, Float64}[]
    for row in CSV.File(filename)
        push!(data, (row.word, row.start_time, row.end_time))
    end
    return data
end

function load_network_data(filename="wireshark_logs/home_mini/home_mini_common_uk_network.csv")
    data = Tuple{Float64, Int}[]
    for row in CSV.File(filename)
        push!(data, (row.time, row.size))
    end
    return data
end

function visualize(word_data, light_data, network_data, company="google")
    trigger_word = company == "google" ? "ok_google" : "hey_alexa"

    lines(network_data, color=:black, label="network packet sizes")

    for (word, start_time, end_time) in word_data
        if word == trigger_word
            linesegments!([(start_time, 0), (start_time, 2000)], color=:blue)
        end
    end

    for (start_time, end_time) in light_data
        lines!([(start_time, -100), (start_time, 0)], color=:red)
    end

    axislegend()
    current_figure()
end

function visualize_data(word_filename, light_filename, network_filename, company="google")
    word_data = load_word_data(word_filename)
    light_data = load_light_data(light_filename)
    network_data = load_network_data(network_filename)

    visualize(word_data, light_data, network_data, company)
end

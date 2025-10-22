use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize)]
pub struct AlgorithmResult {
    pub algorithm_name: String,
    pub parameters: HashMap<String, String>,
    pub route_length: f64,
    pub route: Vec<usize>,
    pub execution_time_ms: u64,
    pub iterations: u32,
    pub start_timestamp: DateTime<Utc>,
    pub additional_metrics: HashMap<String, f64>,
}

impl AlgorithmResult {
    pub fn new(algorithm_name: String) -> Self {
        Self {
            algorithm_name,
            parameters: HashMap::new(),
            route_length: 0.0,
            route: Vec::new(),
            execution_time_ms: 0,
            iterations: 0,
            start_timestamp: Utc::now(),
            additional_metrics: HashMap::new(),
        }
    }

    pub fn with_parameter(mut self, key: String, value: String) -> Self {
        self.parameters.insert(key, value);
        self
    }

    pub fn with_metric(mut self, key: String, value: f64) -> Self {
        self.additional_metrics.insert(key, value);
        self
    }

    pub fn set_result(mut self, route_length: f64, route: Vec<usize>) -> Self {
        self.route_length = route_length;
        self.route = route;
        self
    }

    pub fn set_execution_time(mut self, time_ms: u64) -> Self {
        self.execution_time_ms = time_ms;
        self
    }

    pub fn set_iterations(mut self, iterations: u32) -> Self {
        self.iterations = iterations;
        self
    }
}

pub struct ResultMonitor {
    results_dir: String,
}

impl ResultMonitor {
    pub fn new() -> Self {
        let results_dir = "wyniki".to_string();
        Self { results_dir }
    }

    pub fn save_result(&self, result: &AlgorithmResult) -> Result<String, Box<dyn std::error::Error>> {
        // Ensure results directory exists
        if !Path::new(&self.results_dir).exists() {
            fs::create_dir_all(&self.results_dir)?;
        }

        // Create filename with algorithm name and timestamp
        let timestamp = result.start_timestamp.format("%Y%m%d_%H%M%S_%3f");
        let filename = format!("{}_{}.json", result.algorithm_name, timestamp);
        let filepath = Path::new(&self.results_dir).join(&filename);

        // Serialize to JSON
        let json = serde_json::to_string_pretty(result)?;

        // Write to file
        fs::write(&filepath, json)?;

        Ok(filename)
    }

    pub fn list_results(&self) -> Result<Vec<String>, Box<dyn std::error::Error>> {
        if !Path::new(&self.results_dir).exists() {
            return Ok(Vec::new());
        }

        let mut files = Vec::new();
        for entry in fs::read_dir(&self.results_dir)? {
            let entry = entry?;
            if entry.path().extension().and_then(|s| s.to_str()) == Some("json") {
                if let Some(filename) = entry.file_name().to_str() {
                    files.push(filename.to_string());
                }
            }
        }
        files.sort();
        Ok(files)
    }
}

impl Default for ResultMonitor {
    fn default() -> Self {
        Self::new()
    }
}
